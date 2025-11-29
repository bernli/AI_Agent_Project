"""Test script to verify key imports work correctly."""

import sys

print("=" * 60)
print("Testing InsightLoop Imports")
print("=" * 60)

errors = []

# Test 1: Config imports
print("\n[1/4] Testing config imports...")
try:
    from .config import MAIN_AGENT_MODEL, MAX_RETRIES
    print(f"  OK - MAIN_AGENT_MODEL: {MAIN_AGENT_MODEL}")
    print(f"  OK - MAX_RETRIES: {MAX_RETRIES}")
except Exception as e:
    errors.append(f"Config import failed: {e}")
    print(f"  FAILED: {e}")

# Test 2: Tools imports
print("\n[2/4] Testing tools imports...")
try:
    from .tools import analyze_dataframe, execute_python_analysis, style_chart
    print("  OK - analyze_dataframe")
    print("  OK - execute_python_analysis")
    print("  OK - style_chart")
except Exception as e:
    errors.append(f"Tools import failed: {e}")
    print(f"  FAILED: {e}")

# Test 3: Sub-agent imports
print("\n[3/4] Testing sub-agent imports...")
try:
    from .sub_agents.code_writer import code_writer_agent
    print(f"  OK - code_writer_agent: {code_writer_agent.name}")
except Exception as e:
    errors.append(f"code_writer import failed: {e}")
    print(f"  FAILED: {e}")

try:
    from .sub_agents.validation_checkers import (
        CodeValidationChecker,
        CodeSafetyChecker,
        ExecutionRunner,
        ExecutionValidationChecker,
    )
    print(f"  OK - CodeValidationChecker")
    print(f"  OK - CodeSafetyChecker")
    print(f"  OK - ExecutionRunner")
    print(f"  OK - ExecutionValidationChecker")
except Exception as e:
    errors.append(f"validation_checkers import failed: {e}")
    print(f"  FAILED: {e}")

try:
    from .sub_agents.code_review_loop import robust_code_generator
    print(f"  OK - robust_code_generator: {robust_code_generator.name}")
    print(f"       Sub-agents: {[a.name for a in robust_code_generator.sub_agents]}")
except Exception as e:
    errors.append(f"code_review_loop import failed: {e}")
    print(f"  FAILED: {e}")

# Test 4: Main agent import
print("\n[4/4] Testing main agent import...")
try:
    from .agent import root_agent, interactive_analyst_agent
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
