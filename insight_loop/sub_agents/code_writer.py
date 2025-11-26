"""Code Writer Sub-Agent - Generates Python/Pandas code for data analysis."""

from google.adk.agents import Agent
from ..config import WORKER_MODEL
from ..agent_utils import suppress_output_callback


code_writer_agent = Agent(
    name="code_writer",
    model=WORKER_MODEL,
    description="Writes Python/Pandas code to answer data analysis questions.",
    instruction="""
You are a Python data analyst. Return ONLY the Python code, no explanations or summaries.

Context:
- dataframe_context: {dataframe_context?}
- Previous feedback: {review_result?}

Rules:
- df is pre-loaded, don't use pd.read_csv()
- Store result in `result_value` (scalar) or `result_df` (DataFrame)
- End with: # FILE_PATH: [path from dataframe_context]
- Do not add any text outside the code

If feedback says NEEDS_REVISION, fix those issues and return code only.
""",
    output_key="generated_code",
    after_agent_callback=suppress_output_callback
)
