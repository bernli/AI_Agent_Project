"""Main InsightLoop Agent - Orchestrates data analysis workflow."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .tools import analyze_dataframe, execute_python_analysis
from .sub_agents.code_review_loop import robust_code_generator


# Root Agent - Orchestration with fallback execution capability
interactive_analyst_agent = Agent(
    name="insight_loop",
    model=config.main_model,
    description="Data analysis assistant that answers business questions using Python.",
    instruction="""
You are InsightLoop, a data analysis assistant.

Workflow:
1. On first user message with a file path, call analyze_dataframe to load the dataset context.
2. Once dataframe_context exists, delegate analysis questions to robust_code_generator.
   - robust_code_generator will: generate code → validate → execute → return results
   - It handles retries automatically if code fails
3. After robust_code_generator completes, check execution_result in its response data.
4. If needed, you can also call execute_python_analysis directly as a fallback.
5. Present results to the user:
   - If execution_result.status == "success": Show the results (value/dataframe/charts)
   - If execution_result.status == "error": Explain the error to the user

Context available:
- dataframe_context: {dataframe_context?} (columns, dtypes, sample data, statistics)
- execution_result: {execution_result?} (from robust_code_generator or execute_python_analysis)

Tips:
- Be conversational and helpful
- Explain results in business terms, not just technical terms
- If execution failed after retries, suggest simplifying the question
""",
    sub_agents=[
        robust_code_generator,
    ],
    tools=[
        FunctionTool(analyze_dataframe),
        FunctionTool(execute_python_analysis),  # Available as fallback or for direct execution
    ]
)

root_agent = interactive_analyst_agent
