"""Configuration for InsightLoop agents."""

# Model configuration - Using Gemini 2.5 Flash
PLANNER_MODEL = "gemini-2.5-flash"
PYTHON_EXECUTOR_MODEL = "gemini-2.5-flash"
SQL_EXECUTOR_MODEL = "gemini-2.5-flash"
CHART_STYLER_MODEL = "gemini-2.5-flash"
INSIGHT_REVIEWER_MODEL = "gemini-2.5-flash"
MAIN_AGENT_MODEL = "gemini-2.5-flash"

# Retry configuration for LoopAgents
MAX_RETRIES = 3

# Chart styling configuration
CHART_DPI = 300
CHART_STYLE = "seaborn-v0_8-darkgrid"
COLOR_PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
