"""Code Writer Sub-Agent - Generates Python/Pandas code for data analysis."""

from google.adk.agents import Agent
from ..config import WORKER_MODEL


code_writer_agent = Agent(
    name="code_writer",
    model=WORKER_MODEL,
    description="Writes Python/Pandas code to answer data analysis questions.",
    instruction="""
You are a Python data analyst. Write code to answer the user's question.

Context:
- dataframe_context: {dataframe_context?}
- Previous feedback: {review_result?}

Rules:
- df is pre-loaded, don't use pd.read_csv()
- Store result in `result_value` (scalar) or `result_df` (DataFrame)
- End with: # FILE_PATH: [path from dataframe_context]

If feedback says NEEDS_REVISION, fix those issues.
""",
    output_key="generated_code"
)
