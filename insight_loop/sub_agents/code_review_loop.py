"""Code Review Loop - Iterates between code writing and reviewing until approved."""

from google.adk.agents import LoopAgent
from ..config import MAX_RETRIES
from .code_writer import code_writer_agent
from .validation_checkers import CodeValidationChecker


# Simplified LoopAgent pattern (like Agent-Shutton's blog_planner)
# Flow: code_writer -> validation_checker
# Exits when: CodeValidationChecker finds generated_code exists (escalates)

robust_code_generator = LoopAgent(
    name="robust_code_generator",
    description="Generates Python code until valid.",
    sub_agents=[
        code_writer_agent,
        CodeValidationChecker(name="code_validation_checker"),
    ],
    max_iterations=MAX_RETRIES
)
