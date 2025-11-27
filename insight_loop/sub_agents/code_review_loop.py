"""Code Review Loop - Iterates between code writing and reviewing until approved."""

from google.adk.agents import LoopAgent
from ..config import MAX_RETRIES
from ..agent_utils import suppress_output_callback
from .code_writer import code_writer_agent
from .validation_checkers import (
    CodeValidationChecker,
    CodeSafetyChecker,
    ExecutionRunner,
    ExecutionReturner,
)


# Simplified LoopAgent pattern
# Flow: code_writer -> safety_checker -> validation_checker -> execution_runner -> execution_returner
# Exits when: execution_returner escalates (on success OR failure after showing result)
# Retries: If validation fails, loop continues until MAX_RETRIES

robust_code_generator = LoopAgent(
    name="robust_code_generator",
    description="Generates Python code until valid.",
    sub_agents=[
        code_writer_agent,
        CodeSafetyChecker(name="code_safety_checker"),
        CodeValidationChecker(name="code_validation_checker"),
        ExecutionRunner(name="code_executor"),
        ExecutionReturner(name="execution_returner"),
    ],
    max_iterations=MAX_RETRIES,
    after_agent_callback=suppress_output_callback,  # Simplified: no fancy feedback
)
