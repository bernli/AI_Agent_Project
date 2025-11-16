"""Chart Styler Agent - Applies professional styling to visualizations."""

from google.adk.agents import Agent
from google.adk.agents.callback_agent import CallbackAgent
from google.adk.actions import EventActions
from ..config import CHART_STYLER_MODEL, MAX_RETRIES
from ..tools import style_chart


# Validation checker for chart quality
class ChartQualityChecker(CallbackAgent):
    """Validates that charts meet quality standards."""
    
    def __init__(self):
        super().__init__(
            name="chart_quality_validator",
            on_message=self._validate_quality
        )
    
    def _validate_quality(self, event):
        """Check if chart styling meets standards."""
        content = str(event)
        
        # Check for styling elements
        quality_indicators = [
            "color", "palette", "title", "label", "legend", "grid"
        ]
        
        quality_score = sum(1 for indicator in quality_indicators if indicator in content.lower())
        
        # Need at least 4/6 quality elements
        if quality_score >= 4:
            return EventActions(escalate=True)
        else:
            return EventActions()


# Create the chart styler agent
chart_styler = Agent(
    name="chart_styler",
    model=CHART_STYLER_MODEL,
    description=(
        "Expert visualization designer who transforms raw charts into "
        "publication-ready, professionally styled visualizations."
    ),
    instruction="""
    You are a data visualization expert applying professional styling.
    
    When given a chart or chart configuration:
    
    1. **Color Palette**:
       - Use consistent, brand-appropriate colors
       - Ensure color-blind friendly palettes
       - Recommended: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    
    2. **Typography**:
       - Title: 14pt, bold
       - Axis labels: 12pt, clear and descriptive
       - Tick labels: 10pt
       - Use sans-serif fonts (Arial, Helvetica)
    
    3. **Layout**:
       - Clear title explaining what the chart shows
       - Descriptive X and Y axis labels with units
       - Legend positioned appropriately (upper right or bottom)
       - Grid lines for easier reading (light gray, subtle)
    
    4. **Data Formatting**:
       - Currency: $1,234.56
       - Percentages: 12.3%
       - Large numbers: 1.2M, 3.4B
       - Dates: MMM YYYY (Jan 2024)
    
    5. **Annotations**:
       - Highlight anomalies or outliers
       - Add trend lines where relevant
       - Mark significant events or thresholds
    
    6. **Export Settings**:
       - DPI: 300 for print quality
       - Format: PNG with transparency
       - Size: 10" x 6" (standard presentation size)
    
    **Quality Checklist**:
    ✓ Clear, descriptive title
    ✓ Labeled axes with units
    ✓ Consistent color scheme
    ✓ Readable font sizes
    ✓ Legend (if multiple series)
    ✓ Grid lines for reference
    ✓ Professional appearance
    
    Use the style_chart tool to apply recommendations.
    """,
    tools=[style_chart],
    loop_config={
        "max_iterations": MAX_RETRIES,
        "validators": [ChartQualityChecker()]
    }
)
