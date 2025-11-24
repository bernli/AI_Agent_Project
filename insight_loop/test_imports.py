"""Test script to verify all imports work correctly."""

import sys

print("=" * 60)
print("Testing InsightLoop Imports")
print("=" * 60)

errors = []

# Test 1: Config imports
print("\n[1/6] Testing config imports...")
try:
    from config import MAIN_AGENT_MODEL, MAX_RETRIES
    print(f"  OK - MAIN_AGENT_MODEL: {MAIN_AGENT_MODEL}")
    print(f"  OK - MAX_RETRIES: {MAX_RETRIES}")
except Exception as e:
    errors.append(f"Config import failed: {e}")
    print(f"  FAILED: {e}")

# Test 2: Tools imports
print("\n[2/6] Testing tools imports...")
try:
    from tools import load_csv_data, execute_python_analysis, style_chart
    print("  OK - load_csv_data")
    print("  OK - execute_python_analysis")
    print("  OK - style_chart")
except Exception as e:
    errors.append(f"Tools import failed: {e}")
    print(f"  FAILED: {e}")

# Test 3: Individual sub-agent imports
print("\n[3/6] Testing individual sub-agent imports...")
try:
    from sub_agents.csv_loader import csv_loader_agent
    print(f"  OK - csv_loader_agent: {csv_loader_agent.name}")
except Exception as e:
    errors.append(f"csv_loader import failed: {e}")
    print(f"  FAILED: {e}")

try:
    from sub_agents.code_writer import code_writer_agent
    print(f"  OK - code_writer_agent: {code_writer_agent.name}")
except Exception as e:
    errors.append(f"code_writer import failed: {e}")
    print(f"  FAILED: {e}")

try:
    from sub_agents.code_reviewer import code_reviewer_agent
    print(f"  OK - code_reviewer_agent: {code_reviewer_agent.name}")
except Exception as e:
    errors.append(f"code_reviewer import failed: {e}")
    print(f"  FAILED: {e}")

# Test 4: LoopAgent import
print("\n[4/6] Testing LoopAgent import...")
try:
    from sub_agents.code_review_loop import code_review_loop_agent
    print(f"  OK - code_review_loop_agent: {code_review_loop_agent.name}")
    print(f"       Sub-agents: {[a.name for a in code_review_loop_agent.sub_agents]}")
except Exception as e:
    errors.append(f"LoopAgent import failed: {e}")
    print(f"  FAILED: {e}")

# Test 5: SequentialAgent import
print("\n[5/6] Testing SequentialAgent (analysis_pipeline) import...")
try:
    from sub_agents.analysis_pipeline import analysis_pipeline_agent, code_executor_agent
    print(f"  OK - analysis_pipeline_agent: {analysis_pipeline_agent.name}")
    print(f"       Sub-agents: {[a.name for a in analysis_pipeline_agent.sub_agents]}")
    print(f"  OK - code_executor_agent: {code_executor_agent.name}")
except Exception as e:
    errors.append(f"SequentialAgent import failed: {e}")
    print(f"  FAILED: {e}")

# Test 6: Main agent import
print("\n[6/6] Testing main agent import...")
try:
    from agent import root_agent, interactive_analyst_agent
    print(f"  OK - root_agent: {root_agent.name}")
    print(f"  OK - interactive_analyst_agent: {interactive_analyst_agent.name}")
    print(f"       Sub-agents: {[a.name for a in interactive_analyst_agent.sub_agents]}")
except Exception as e:
    errors.append(f"Main agent import failed: {e}")
    print(f"  FAILED: {e}")

# Summary
print("\n" + "=" * 60)
if errors:
    print(f"FAILED - {len(errors)} error(s) found:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("SUCCESS - All imports working correctly!")
    sys.exit(0)
