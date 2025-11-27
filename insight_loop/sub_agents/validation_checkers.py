"""Validation checkers for InsightLoop agents (Agent-Shutton pattern)."""

import re
from typing import AsyncGenerator, Optional
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from ..tools import execute_python_analysis
from ..config import DISALLOWED_PATTERNS as CONFIG_DISALLOWED_PATTERNS


class CodeValidationChecker(BaseAgent):
    """Minimal gate: ensure generated code exists and a data path is available; escalate when ready."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        generated_code = ctx.session.state.get("generated_code")
        df_ctx = ctx.session.state.get("dataframe_context", {}) or {}
        ctx_file_path = df_ctx.get("file_path") if isinstance(df_ctx, dict) else None
        marker_file_path = _extract_data_path_from_code(generated_code or "")

        if not generated_code:
            ctx.session.state["review_result"] = "NEEDS_REVISION: No code generated."
            yield Event(author=self.name)
            return

        if not ctx_file_path and not marker_file_path:
            ctx.session.state["review_result"] = "NEEDS_REVISION: Add '# FILE_PATH: <path>' so execution can run."
            yield Event(author=self.name)
            return

        ctx.session.state["review_result"] = "APPROVED"
        yield Event(author=self.name, actions=EventActions(escalate=True))


class DataframeValidationChecker(BaseAgent):
    """Checks if dataframe context is loaded."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        if ctx.session.state.get("dataframe_context"):
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name)


class ExecutionValidationChecker(BaseAgent):
    """Checks if code execution was successful (no escalation here)."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        result = ctx.session.state.get("execution_result", {})
        # No escalation; ExecutionReturner will escalate with payload
        yield Event(author=self.name)


class ExecutionReturner(BaseAgent):
    """
    Returns execution_result and decides whether to exit loop or retry.

    Escalates (exits loop) only on SUCCESS.
    Continues loop (no escalate) on FAILURE to trigger retry with improved code.
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        result = ctx.session.state.get("execution_result", {})

        # Build a minimal summary
        if isinstance(result, dict):
            status = result.get("status")
            if status == "success":
                # SUCCESS: Build success summary
                if "value" in result:
                    summary = f"✅ Analysis complete. Result: {result['value']}"
                elif "dataframe" in result:
                    summary = f"✅ Analysis complete. Returned {len(result['dataframe'])} rows."
                elif "charts" in result:
                    summary = f"✅ Analysis complete. Created {len(result['charts'])} chart(s)."
                else:
                    summary = "✅ Analysis complete."

                # Escalate to exit loop - we're done!
                yield Event(
                    author=self.name,
                    content=summary,
                    data={"execution_result": result},
                    actions=EventActions(escalate=True),
                )
            else:
                # FAILURE: Provide feedback for retry
                error_msg = result.get('error_message', 'Unknown error')
                error_type = result.get('error_type', 'Error')

                summary = f"❌ Execution failed ({error_type}): {error_msg}"

                # Set review_result to guide code_writer on next iteration
                ctx.session.state["review_result"] = f"NEEDS_REVISION: {error_msg}"

                # DO NOT escalate - continue loop to retry
                yield Event(
                    author=self.name,
                    content=summary,
                )
        else:
            # Unknown result format - escalate to avoid infinite loop
            summary = "⚠️ Execution completed with unknown result format."
            yield Event(
                author=self.name,
                content=summary,
                data={"execution_result": result},
                actions=EventActions(escalate=True),
            )


class ExecutionRunner(BaseAgent):
    """Executes generated code using execute_python_analysis and stores result."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        generated_code = ctx.session.state.get("generated_code", "")
        data_path = _extract_data_path(ctx, generated_code)

        if not generated_code:
            ctx.session.state["execution_result"] = {
                "status": "error",
                "error_message": "No generated_code to execute."
            }
            yield Event(author=self.name)
            return

        if not data_path:
            ctx.session.state["execution_result"] = {
                "status": "error",
                "error_message": "Missing data_path for execution. Ensure code ends with '# FILE_PATH: <path>' or dataframe_context has file_path."
            }
            yield Event(author=self.name)
            return

        result = execute_python_analysis(code=generated_code, data_path=data_path)
        ctx.session.state["execution_result"] = result
        # Do not escalate here; let ExecutionValidationChecker decide based on result.
        yield Event(author=self.name)


def _extract_data_path(ctx: InvocationContext, code: str) -> Optional[str]:
    """Get data path from dataframe_context or FILE_PATH comment in code."""
    df_ctx = ctx.session.state.get("dataframe_context", {})
    if isinstance(df_ctx, dict) and df_ctx.get("file_path"):
        return df_ctx["file_path"]

    return _extract_data_path_from_code(code)


def _extract_data_path_from_code(code: str) -> Optional[str]:
    """Parse FILE_PATH marker from generated code."""
    import os

    for line in code.splitlines():
        if "file_path" in line.lower():
            # Stricter regex to prevent path traversal: only allows safe path characters
            match = re.search(r"file_path[:=]\s*#?\s*([a-zA-Z0-9_./\\:\-]+)", line, flags=re.IGNORECASE)
            if match:
                path = match.group(1).strip()
                # Additional security: resolve to absolute path and validate
                try:
                    abs_path = os.path.abspath(path)
                    # Only allow paths within current working directory or its subdirectories
                    if abs_path.startswith(os.path.abspath(os.getcwd())):
                        return path
                except (ValueError, OSError):
                    # Invalid path, skip
                    continue
    return None


class CodeSafetyChecker(BaseAgent):
    """Lightweight static checks to catch unsafe or malformed generated code."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        code = ctx.session.state.get("generated_code", "")
        issues = []

        if not code:
            yield Event(author=self.name)
            return

        # Use centralized disallowed patterns from config, plus pd.read_csv specific to this checker
        extended_patterns = list(CONFIG_DISALLOWED_PATTERNS) + ["pd.read_csv"]

        lowered = code.lower()
        for pattern in extended_patterns:
            if pattern in lowered:
                issues.append(f"Disallowed usage detected: {pattern}")

        if "result_df" not in code and "result_value" not in code:
            issues.append("Missing `result_df` or `result_value` assignment.")

        if "df" not in code:
            issues.append("Code should operate on provided `df` context.")

        if issues:
            ctx.session.state["review_result"] = "NEEDS_REVISION: " + "; ".join(issues)
        else:
            ctx.session.state["review_result"] = "APPROVED: Safety checks passed."

        yield Event(author=self.name)
