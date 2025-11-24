"""Validation checkers for InsightLoop agents (Agent-Shutton pattern)."""

import re
from typing import AsyncGenerator, ClassVar, Tuple, Optional
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from ..tools import execute_python_analysis


class CodeValidationChecker(BaseAgent):
    """Checks generated code is present and marks revision status (no execution)."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        generated_code = ctx.session.state.get("generated_code")
        review_result = ctx.session.state.get("review_result", "")
        df_ctx = ctx.session.state.get("dataframe_context", {}) or {}
        ctx_file_path = df_ctx.get("file_path") if isinstance(df_ctx, dict) else None
        marker_file_path = _extract_data_path_from_code(generated_code or "")

        if not generated_code:
            yield Event(author=self.name)
            return

        # Carry forward prior revision flags
        if str(review_result).startswith("NEEDS_REVISION"):
            ctx.session.state["review_result"] = review_result
            yield Event(author=self.name)
            return

        # Require a usable data path
        if not ctx_file_path and not marker_file_path:
            ctx.session.state["review_result"] = "NEEDS_REVISION: Add '# FILE_PATH: <path>' so execution can run."
            yield Event(author=self.name)
            return

        ctx.session.state["review_result"] = "APPROVED: Validation checks passed."

        # Do not escalate; execution agent will decide success/failure.
        yield Event(author=self.name)


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
    """Checks if code execution was successful."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        result = ctx.session.state.get("execution_result", {})
        if isinstance(result, dict) and result.get("status") == "success":
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name)


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
        yield Event(author=self.name, actions=EventActions(escalate=result.get("status") == "success"))


def _extract_data_path(ctx: InvocationContext, code: str) -> Optional[str]:
    """Get data path from dataframe_context or FILE_PATH comment in code."""
    df_ctx = ctx.session.state.get("dataframe_context", {})
    if isinstance(df_ctx, dict) and df_ctx.get("file_path"):
        return df_ctx["file_path"]

    return _extract_data_path_from_code(code)


def _extract_data_path_from_code(code: str) -> Optional[str]:
    """Parse FILE_PATH marker from generated code."""
    for line in code.splitlines():
        if "file_path" in line.lower():
            match = re.search(r"file_path[:=]\s*#?\s*(.*)", line, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip()
    return None


class CodeSafetyChecker(BaseAgent):
    """Lightweight static checks to catch unsafe or malformed generated code."""

    DISALLOWED_PATTERNS: ClassVar[Tuple[str, ...]] = (
        "pd.read_csv",
        "subprocess",
        "os.remove",
        "os.rmdir",
        "shutil.rmtree",
        "requests",
        "http.client",
        "socket",
    )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        code = ctx.session.state.get("generated_code", "")
        issues = []

        if not code:
            yield Event(author=self.name)
            return

        lowered = code.lower()
        for pattern in self.DISALLOWED_PATTERNS:
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
