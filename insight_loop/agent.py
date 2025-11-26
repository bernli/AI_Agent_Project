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
1. On first user message that includes a file path, immediately call analyze_dataframe (do not greet).
2. Once dataframe_context exists, route questions to robust_code_generator to write/review/execute code.
3. After robust_code_generator completes, read execution_result from state. If missing or status != "success", call execute_python_analysis with:
   - code: generated_code
   - data_path: dataframe_context.file_path (or FILE_PATH marker in code)
4. Present results (result_value/result_df, charts, stdout/stderr) to user. Never stop after code generation.

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
    ]
)

root_agent = interactive_analyst_agent
