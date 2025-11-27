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
    state = callback_context.state

    # Check state for important information
    review_result = state.get("review_result", "")
    execution_result = state.get("execution_result", {})

    # Code writer - just show simple message
    if agent_name == "code_writer":
        return Content(parts=[{"text": "📝 Code generated"}])

    # Safety/validation checks - show based on review_result
    if agent_name in ["code_safety_checker", "code_validation_checker"]:
        if review_result:
            if "NEEDS_REVISION" in review_result:
                return Content(parts=[{"text": f"⚠️ {review_result[:200]}"}])
            elif "APPROVED" in review_result:
                return Content(parts=[{"text": "✅ Validation passed"}])
        return Content()

    # Execution runner
    if agent_name == "code_executor":
        if isinstance(execution_result, dict):
            status = execution_result.get("status")
            if status == "success":
                return Content(parts=[{"text": "✅ Code executed successfully"}])
            elif status == "error":
                error_msg = execution_result.get("error_message", "Unknown error")
                return Content(parts=[{"text": f"❌ Execution failed: {error_msg[:200]}"}])
        return Content()

    # Execution returner - show final result
    if agent_name == "execution_returner":
        if isinstance(execution_result, dict):
            status = execution_result.get("status")
            if status == "success":
                if "value" in execution_result:
                    return Content(parts=[{"text": f"✅ Analysis complete. Result: {execution_result['value']}"}])
                elif "dataframe" in execution_result:
                    return Content(parts=[{"text": f"✅ Analysis complete. Returned {len(execution_result['dataframe'])} rows."}])
                elif "charts" in execution_result:
                    return Content(parts=[{"text": f"✅ Analysis complete. Created {len(execution_result['charts'])} chart(s)."}])
                else:
                    return Content(parts=[{"text": "✅ Analysis complete."}])
            else:
                error_msg = execution_result.get("error_message", "Unknown error")
                return Content(parts=[{"text": f"❌ Execution failed: {error_msg[:200]}"}])
        return Content()

    # For other agents, suppress output
    return Content()
