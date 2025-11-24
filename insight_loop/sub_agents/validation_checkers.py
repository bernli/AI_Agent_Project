"""Validation checkers for InsightLoop agents (Agent-Shutton pattern)."""

from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions


class CodeValidationChecker(BaseAgent):
    """Checks if generated code exists (like Agent-Shutton's OutlineValidationChecker)."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Simple check: does generated_code exist?
        if ctx.session.state.get("generated_code"):
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
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
