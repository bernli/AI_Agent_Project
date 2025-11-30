"""Test script to list available BigQuery MCP tools."""

import asyncio
from pathlib import Path
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams

PROJECT_ROOT = Path(__file__).parent.absolute()

async def test_mcp_tools():
    """List all available BigQuery MCP tools."""
    print("=" * 60)
    print("Testing BigQuery MCP Toolset")
    print("=" * 60)

    # Create toolset WITHOUT filter
    toolset = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=str(PROJECT_ROOT / "mcp-toolbox" / "toolbox-bigquery.exe"),
                args=["--prebuilt", "bigquery", "--stdio"],
                env={
                    "BIGQUERY_PROJECT": "gen-lang-client-0152066550",
                    "GOOGLE_APPLICATION_CREDENTIALS": str(PROJECT_ROOT / "mcp-toolbox" / "service-account-key.json")
                }
            ),
            timeout=10
        )
    )

    print("\n1. Loading tools WITHOUT filter...")
    tools = await toolset.get_tools()
    print(f"\n   Found {len(tools)} tools:")
    for i, tool in enumerate(tools, 1):
        print(f"   {i}. {tool.name}")

    await toolset.close()

    # Create toolset WITH filter
    print("\n" + "=" * 60)
    print("\n2. Loading tools WITH filter ['execute_sql', 'ask_data_insights', 'analyze_contribution']...")

    toolset_filtered = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=str(PROJECT_ROOT / "mcp-toolbox" / "toolbox-bigquery.exe"),
                args=["--prebuilt", "bigquery", "--stdio"],
                env={
                    "BIGQUERY_PROJECT": "gen-lang-client-0152066550",
                    "GOOGLE_APPLICATION_CREDENTIALS": str(PROJECT_ROOT / "mcp-toolbox" / "service-account-key.json")
                }
            ),
            timeout=10
        ),
        tool_filter=["execute_sql", "ask_data_insights", "analyze_contribution"]
    )

    tools_filtered = await toolset_filtered.get_tools()
    print(f"\n   Found {len(tools_filtered)} tools:")
    for i, tool in enumerate(tools_filtered, 1):
        print(f"   {i}. {tool.name}")

    await toolset_filtered.close()

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
