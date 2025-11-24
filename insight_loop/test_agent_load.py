"""Test if the agent can be loaded successfully."""

import sys
import os

# Add parent directory to path so we can import insight_loop as a package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing agent loading...")
print("=" * 50)

try:
    # Test 1: Import main agent
    print("\n[1/4] Importing main agent module...")
    from insight_loop.agent import interactive_analyst_agent, root_agent
    print("      [OK] Main agent imported")

    # Test 2: Check agent structure
    print("\n[2/4] Checking agent structure...")
    print(f"      Agent name: {interactive_analyst_agent.name}")
    print(f"      Agent model: {interactive_analyst_agent.model}")
    print(f"      Sub-agents: {len(interactive_analyst_agent.sub_agents)}")
    print(f"      Tools: {len(interactive_analyst_agent.tools)}")
    print("      [OK] Agent structure valid")

    # Test 3: Check sub-agents
    print("\n[3/4] Checking sub-agents...")
    for sub_agent in interactive_analyst_agent.sub_agents:
        print(f"      - {sub_agent.name}")
    print("      [OK] All sub-agents loaded")

    # Test 4: Check tools
    print("\n[4/4] Checking tools...")
    for tool in interactive_analyst_agent.tools:
        print(f"      - {tool.__name__}")
    print("      [OK] All tools loaded")

    print("\n" + "=" * 50)
    print("SUCCESS! Agent ist vollstaendig ladefaehig!")
    print("=" * 50)

    print("\nNaechste Schritte:")
    print("1. cd ..")
    print("2. adk web")
    print("3. Browser oeffnen: http://localhost:8000")

except Exception as e:
    print(f"\n[ERROR] Agent konnte nicht geladen werden:")
    print(f"        {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
