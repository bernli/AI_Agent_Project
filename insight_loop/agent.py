"""Main InsightLoop Agent - Orchestrates data analysis workflow."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .tools import analyze_dataframe, execute_python_analysis
from .sub_agents.code_review_loop import robust_code_generator


# Root Agent - Like Agent-Shutton pattern
interactive_analyst_agent = Agent(
    name="insight_loop",
    model=config.main_model,
    description="Data analysis assistant that answers business questions using Python.",
    instruction="""
You are InsightLoop, a data analysis assistant.

Workflow:
1. User provides CSV path → call analyze_dataframe to get context
2. User asks question → use robust_code_generator to write and review code
3. After robust_code_generator completes, extract code and file_path, then call execute_python_analysis directly
4. Present results to user

Context:
- dataframe_context: {dataframe_context?}
- generated_code: {generated_code?}
- execution_result: {execution_result?}

IMPORTANT: After robust_code_generator finishes, YOU must call execute_python_analysis with:
- code: the generated Python code (from generated_code)
- data_path: the CSV file path (from dataframe_context or FILE_PATH comment in code)
""",
    sub_agents=[
        robust_code_generator,
    ],
    tools=[
        FunctionTool(analyze_dataframe),
        FunctionTool(execute_python_analysis),
    ],
    output_key="dataframe_context"
)

root_agent = interactive_analyst_agent
