"""Analysis Planner Agent - Creates structured analysis plans."""

from google.adk.agents import Agent
from google.adk.agents.callback_agent import CallbackAgent
from google.adk.actions import EventActions
from ..config import PLANNER_MODEL, MAX_RETRIES


# Validation checker for analysis plans
class PlanValidationChecker(CallbackAgent):
    """Validates that analysis plans are complete and executable."""
    
    def __init__(self):
        super().__init__(
            name="plan_validator",
            on_message=self._validate_plan
        )
    
    def _validate_plan(self, event):
        """Check if the analysis plan is valid."""
        plan_content = str(event)
        
        # Basic validation: check for key sections
        required_elements = [
            "1.",  # Plan should be numbered
            "filter" or "select" or "group",  # Should have data operations
        ]
        
        has_structure = any(elem in plan_content.lower() for elem in required_elements)
        
        if has_structure and len(plan_content) > 100:
            # Plan looks good, escalate to proceed
            return EventActions(escalate=True)
        else:
            # Plan needs improvement, don't escalate (will retry)
            return EventActions()


# Create the analysis planner agent
robust_analysis_planner = Agent(
    name="analysis_planner",
    model=PLANNER_MODEL,
    description=(
        "Expert strategic analyst who creates comprehensive data analysis plans. "
        "Analyzes business questions and dataset schemas to determine required "
        "transformations, filters, aggregations, and visualizations."
    ),
    instruction="""
    You are a strategic data analyst creating analysis plans.
    
    When given a business question and dataset schema:
    
    1. **Understand the Intent**: What is the user really asking?
    2. **Examine the Data**: Review columns, data types, sample rows
    3. **Plan Operations**: 
       - What filters are needed?
       - What aggregations (sum, count, average)?
       - What groupings (by region, by date)?
       - What calculations (growth rates, percentages)?
    4. **Plan Visualizations**:
       - What chart types (bar, line, scatter)?
       - What should be on X and Y axes?
    5. **Output Format**:
       Create a numbered list of steps like:
       
       1. Filter data where date >= '2024-01-01'
       2. Group by region
       3. Calculate sum(revenue) for each group
       4. Compute month-over-month growth rates
       5. Create bar chart: regions on X-axis, revenue on Y-axis
       6. Create line chart: months on X-axis, growth rate on Y-axis
       7. Identify top 3 and bottom 3 performers
    
    Be specific and executable. Each step should be clear enough that an analyst
    can implement it in Python or SQL.
    """,
    # Loop configuration for retries if validation fails
    loop_config={
        "max_iterations": MAX_RETRIES,
        "validators": [PlanValidationChecker()]
    }
)
