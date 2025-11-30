"""Test script to list all available tools from the agent."""

import sys
import asyncio
from pathlib import Path

# Add analytics_agent to path
sys.path.insert(0, str(Path(__file__).parent))

from analytics_agent.agent import interactive_analyst_agent


async def test_agent_tools():
    """List all available tools from the analytics agent."""
    print("=" * 60)
    print("Analytics Agent - Available Tools")
    print("=" * 60)

    try:
        # Access tools directly from the agent
        tools = interactive_analyst_agent.tools

        print(f"\nAgent loaded successfully!")
        print(f"\nTotal tools available: {len(tools)}\n")

        # Group tools by type
        function_tools = []
        mcp_tools = []

        for tool in tools:
            tool_type = type(tool).__name__

            # FunctionTool has a _func attribute, McpToolset is different
            if tool_type == 'FunctionTool':
                if hasattr(tool, '_func'):
                    function_tools.append(tool._func.__name__)
                elif hasattr(tool, 'name'):
                    function_tools.append(tool.name)
            elif tool_type == 'McpToolset':
                mcp_tools.append("BigQuery MCP Toolset")

        # Display Function Tools
        if function_tools:
            print("[Function Tools]")
            for i, name in enumerate(function_tools, 1):
                print(f"   {i}. {name}")

        # Display MCP Tools (BigQuery)
        if mcp_tools:
            print(f"\n[MCP Toolsets]")
            for i, name in enumerate(mcp_tools, 1):
                print(f"   {i}. {name}")
            print("\n   NOTE: MCP tools are loaded dynamically when agent runs.")
            print("   Expected: 9 BigQuery tools (execute_sql, ask_data_insights, etc.)")
        else:
            print("\n[!] WARNING: No BigQuery MCP toolset found!")

        print("\n" + "=" * 60)

        # Check if we have the expected tools
        if len(tools) == 3 and len(function_tools) == 2 and len(mcp_tools) == 1:
            print("SUCCESS: Agent configured with 2 function tools + 1 MCP toolset")
            print("  - Function tools: analyze_dataframe, execute_python_analysis")
            print("  - MCP toolset: BigQuery (9 tools will load at runtime)")
        else:
            print(f"WARNING: Expected 3 items (2 function + 1 toolset), got {len(tools)}")

        print("=" * 60)

    except Exception as e:
        print(f"\nERROR loading agent: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent_tools())
