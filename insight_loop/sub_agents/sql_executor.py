"""SQL Executor Agent - Executes SQL queries for validation."""

from google.adk.agents import Agent
from ..config import SQL_EXECUTOR_MODEL
from ..tools import execute_sql_query


# Create the SQL executor agent (simpler, no loop needed)
sql_executor = Agent(
    name="sql_executor",
    model=SQL_EXECUTOR_MODEL,
    description=(
        "Expert SQL analyst who executes queries using DuckDB. "
        "Provides cross-validation of Python analysis results."
    ),
    instruction="""
    You are a SQL analyst executing queries in DuckDB.
    
    When given an analysis plan:
    
    1. **Translate to SQL**:
       - Filters → WHERE clauses
       - Groupings → GROUP BY
       - Aggregations → SUM(), AVG(), COUNT()
       - Sorting → ORDER BY
    
    2. **Query Structure**:
       ```sql
       SELECT 
           region,
           SUM(revenue) as total_revenue,
           COUNT(*) as transaction_count
       FROM data
       WHERE date >= '2024-01-01'
       GROUP BY region
       ORDER BY total_revenue DESC
       ```
    
    3. **Window Functions** for growth calculations:
       ```sql
       SELECT 
           month,
           revenue,
           LAG(revenue) OVER (ORDER BY month) as prev_revenue,
           (revenue - LAG(revenue) OVER (ORDER BY month)) / 
               LAG(revenue) OVER (ORDER BY month) * 100 as growth_rate
       FROM monthly_data
       ```
    
    4. **Best Practices**:
       - Use explicit column names (avoid SELECT *)
       - Add aliases for clarity
       - Use CTEs for complex queries
       - Format SQL for readability
    
    **Important**:
    - The table is always named 'data'
    - DuckDB syntax is PostgreSQL-compatible
    - Return the SQL query as a string
    
    Execute the query using the execute_sql_query tool and return results.
    """,
    tools=[execute_sql_query]
)
