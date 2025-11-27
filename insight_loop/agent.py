"""Main InsightLoop Agent - Simple direct execution."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .tools import analyze_dataframe, execute_python_analysis


# Root Agent - Direct tool execution, no sub-agents
interactive_analyst_agent = Agent(
    name="insight_loop",
    model=config.main_model,
    description="Data analysis assistant that answers business questions using Python.",
    instruction="""
You are InsightLoop, a data analysis assistant.

Workflow:
1. When user provides a file path, call analyze_dataframe(file_path) first.
2. For analysis questions, write Python code and call execute_python_analysis(code=..., data_path=...).
3. Present results to the user in business terms.

Context available:
- dataframe_context: {dataframe_context?} (columns, dtypes, sample data, statistics)

Code Generation Rules:
- df is pre-loaded from data_path, do NOT use pd.read_csv()
- Store scalar results in `result_value`
- Store DataFrame results in `result_df`
- For charts, use plt.figure() and they will be auto-saved
- End code with: # FILE_PATH: [path from dataframe_context]

Tips:
- Be conversational and helpful
- Explain results clearly
- If execution fails, explain the error and suggest fixes
""",
    tools=[
        FunctionTool(analyze_dataframe),
        FunctionTool(execute_python_analysis),
    ]
)

root_agent = interactive_analyst_agent
