"""Agent utility callbacks for InsightLoop."""

from google.adk.agents.callback_context import CallbackContext
from google.genai.types import Content


def suppress_output_callback(callback_context: CallbackContext) -> Content:
    """
    DEPRECATED: Use selective_feedback_callback instead.
    Suppress agent output by returning an empty Content object.
    """
    return Content()


def selective_feedback_callback(callback_context: CallbackContext) -> Content:
    """
    Provide selective feedback to users - show important messages, suppress verbose details.

    Shows:
    - Status changes (APPROVED, NEEDS_REVISION)
    - Execution results
    - Error messages

    Suppresses:
    - Verbose code output
    - Internal validation details
    """
    agent_name = callback_context.agent_name
    response = callback_context.response

    # Extract text content if available
    if not response or not response.candidates:
        return Content()

    text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text'):
            text += part.text

    # Determine if this is important feedback
    important_keywords = [
        "approved", "needs_revision", "error", "failed", "success",
        "executing", "generating", "analyzing", "completed"
    ]

    text_lower = text.lower()
    is_important = any(keyword in text_lower for keyword in important_keywords)

    # Code writer outputs code - suppress that (too verbose)
    if agent_name == "code_writer":
        return Content(parts=[{"text": "📝 Code generated"}])

    # Safety/validation checks - show if there are issues
    if agent_name in ["code_safety_checker", "code_validation_checker"]:
        if "needs_revision" in text_lower or "error" in text_lower:
            return Content(parts=[{"text": f"⚠️ Validation: {text[:200]}"}])
        elif "approved" in text_lower:
            return Content(parts=[{"text": "✅ Validation passed"}])
        return Content()

    # Execution - always show
    if agent_name in ["code_executor", "execution_returner"]:
        if "success" in text_lower:
            return Content(parts=[{"text": "✅ Execution completed"}])
        elif "error" in text_lower:
            return Content(parts=[{"text": f"❌ Execution failed: {text[:300]}"}])
        return response.candidates[0].content

    # For other agents, show if important
    if is_important:
        return response.candidates[0].content

    return Content()
