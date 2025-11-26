"""Agent utility callbacks for InsightLoop."""

from google.adk.agents.callback_context import CallbackContext
from google.genai.types import Content


def suppress_output_callback(callback_context: CallbackContext) -> Content:
    """Suppress agent output by returning an empty Content object."""
    return Content()
