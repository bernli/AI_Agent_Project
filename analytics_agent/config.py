"""Configuration for Analytics Agent."""

from dataclasses import dataclass


@dataclass
class AnalyticsAgentConfig:
    """Configuration for Analytics Agent system."""
    # Model configuration
    main_model: str = "gemini-2.5-flash"
    worker_model: str = "gemini-2.5-flash"

    # Retry configuration
    max_retries: int = 3

    # Security: Disallowed patterns in generated code
    disallowed_patterns: tuple = (
        "os.remove",
        "os.rmdir",
        "shutil.rmtree",
        "subprocess",
        "requests",
        "socket",
        "http.client",
    )

    # Chart styling
    chart_dpi: int = 300
    chart_style: str = "seaborn-v0_8-darkgrid"
    color_palette: tuple = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd")


# Default configuration instance
config = AnalyticsAgentConfig()

# Export individual values for convenience
MAIN_AGENT_MODEL = config.main_model
WORKER_MODEL = config.worker_model
MAX_RETRIES = config.max_retries
DISALLOWED_PATTERNS = config.disallowed_patterns
CHART_DPI = config.chart_dpi
CHART_STYLE = config.chart_style
COLOR_PALETTE = list(config.color_palette)
