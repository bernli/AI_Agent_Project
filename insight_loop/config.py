"""Configuration for InsightLoop agents."""

from dataclasses import dataclass


@dataclass
class InsightLoopConfig:
    """Configuration for InsightLoop agent system."""
    # Model configuration
    main_model: str = "gemini-2.5-pro"
    worker_model: str = "gemini-2.5-flash"

    # Retry configuration
    max_retries: int = 3

    # Chart styling
    chart_dpi: int = 300
    chart_style: str = "seaborn-v0_8-darkgrid"
    color_palette: tuple = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd")


# Default configuration instance
config = InsightLoopConfig()

# Export individual values for convenience
MAIN_AGENT_MODEL = config.main_model
WORKER_MODEL = config.worker_model
MAX_RETRIES = config.max_retries
CHART_DPI = config.chart_dpi
CHART_STYLE = config.chart_style
COLOR_PALETTE = list(config.color_palette)
