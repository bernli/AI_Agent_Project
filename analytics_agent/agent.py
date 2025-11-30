"""Main Analytics Agent - Simple direct execution."""

from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from .config import config
from .tools import analyze_dataframe, execute_python_analysis


# Get project root directory (parent of analytics_agent)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# BigQuery MCP Toolset
# NOTE: Only expose tools that work with public datasets
# Metadata tools (get_table_info, list_table_ids, get_dataset_info) fail on bigquery-public-data
bigquery_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=str(PROJECT_ROOT / "mcp-toolbox" / "toolbox-bigquery.exe"),
            args=["--prebuilt", "bigquery", "--stdio"],
            env={
                "BIGQUERY_PROJECT": "gen-lang-client-0152066550",
                "GOOGLE_APPLICATION_CREDENTIALS": str(PROJECT_ROOT / "mcp-toolbox" / "service-account-key.json")
            }
        ),
        timeout=10  # Connection timeout in seconds
    ),
    # Whitelist: Only allow these tools (blocks metadata tools that fail on public datasets)
    allowed_tools=["execute_sql", "ask_data_insights", "analyze_contribution"]
)

# Root Agent - Direct tool execution, no sub-agents
interactive_analyst_agent = Agent(
    name="analytics_agent",
    model=config.main_model,
    description="Data analysis assistant that answers business questions using Python.",
    instruction="""
You are Analytics Agent, a data analysis assistant.

DATA SOURCES:
1. **BigQuery E-Commerce** (keywords: "ecommerce", "USA", "America", "North America")
   - Dataset: bigquery-public-data.thelook_ecommerce
   - Tables: orders, products, users, order_items, distribution_centers, events, inventory_items

2. **Local CSV - Canadian Webshop** (keywords: "Canada", "canadian", "neuer webshop", "CSV", file path)
   - Use: analyze_dataframe() → execute_python_analysis()

BIGQUERY TOOL SELECTION:
- **Default:** execute_sql (fast, predictable)
  Use fully-qualified names: `bigquery-public-data`.`thelook_ecommerce`.`orders`
  ⚠️ NEVER use get_table_info, list_table_ids, get_dataset_info - they fail on public datasets!

- **For "why/what caused" questions:** analyze_contribution OR ask_data_insights
  - analyze_contribution: Deep causal analysis with ML
    ⚠️ ALWAYS warn user BEFORE calling: "Running contribution analysis, this takes ~1 minute..."
  - ask_data_insights: Quick exploratory analysis (~10 sec)
    Use for initial "why" questions, then offer analyze_contribution for deeper analysis

- **For open exploration:** ask_data_insights
  Example: "What patterns exist in orders?"

PYTHON (Local CSV):
- df is pre-loaded, do NOT use pd.read_csv()
- Store results in `result_value` or `result_df`
- End with: # FILE_PATH: [path]

MISSING DATA:
- Check data availability first
- Be transparent when data doesn't exist
- Suggest alternatives with available data
- Never make up data
""",
    tools=[
        FunctionTool(analyze_dataframe),
        FunctionTool(execute_python_analysis),
        bigquery_mcp,  # BigQuery MCP Tools
    ]
)

root_agent = interactive_analyst_agent
