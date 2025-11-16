"""Python Executor Agent - Executes pandas/matplotlib analysis."""

from google.adk.agents import Agent
from google.adk.agents.callback_agent import CallbackAgent
from google.adk.actions import EventActions
from ..config import PYTHON_EXECUTOR_MODEL, MAX_RETRIES
from ..tools import execute_python_analysis


# Validation checker for Python execution
class PythonOutputValidationChecker(CallbackAgent):
    """Validates that Python code executed successfully."""
    
    def __init__(self):
        super().__init__(
            name="python_validator",
            on_message=self._validate_output
        )
    
    def _validate_output(self, event):
        """Check if Python execution was successful."""
        output_content = str(event)
        
        # Check for success indicators
        if "success" in output_content.lower() or "result" in output_content.lower():
            return EventActions(escalate=True)
        elif "error" in output_content.lower():
            # Execution failed, don't escalate (will retry)
            return EventActions()
        else:
            # Unclear result, allow to proceed
            return EventActions(escalate=True)


# Create the Python executor agent
robust_python_executor = Agent(
    name="python_executor",
    model=PYTHON_EXECUTOR_MODEL,
    description=(
        "Expert Python data scientist who executes data analysis using pandas, "
        "numpy, and matplotlib. Transforms analysis plans into working code."
    ),
    instruction="""
    You are a Python data scientist executing analysis plans.
    
    When given an analysis plan and dataset:
    
    1. **Import Libraries**:
       ```python
       import pandas as pd
       import numpy as np
       import matplotlib.pyplot as plt
       ```
    
    2. **Load Data**:
       ```python
       df = pd.read_csv('data.csv')
       ```
    
    3. **Execute Each Step** from the plan:
       - Apply filters: df[df['date'] >= '2024-01-01']
       - Group data: df.groupby('region')
       - Aggregate: .agg({'revenue': 'sum'})
       - Calculate: growth_rate = (current - previous) / previous * 100
    
    4. **Create Visualizations**:
       ```python
       plt.figure(figsize=(10, 6))
       plt.bar(x_data, y_data)
       plt.title('Revenue by Region')
       plt.xlabel('Region')
       plt.ylabel('Revenue ($)')
       ```
    
    5. **Store Results**:
       - Save DataFrames as: result_df = ...
       - Save values as: result_value = ...
    
    **Important**:
    - Handle missing data appropriately
    - Use descriptive variable names
    - Add comments to explain complex operations
    - Check data types before operations
    - Handle potential errors (try/except where needed)
    
    Return the complete, executable Python code.
    """,
    tools=[execute_python_analysis],
    loop_config={
        "max_iterations": MAX_RETRIES,
        "validators": [PythonOutputValidationChecker()]
    }
)
