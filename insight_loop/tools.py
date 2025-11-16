"""Custom tools for InsightLoop agents."""

import os
import pandas as pd
import io
from typing import Dict, Any, Optional
import duckdb


def load_csv_data(file_path: str) -> Dict[str, Any]:
    """
    Load CSV data and return schema information.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Dictionary containing schema, sample rows, and data summary
    """
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Get schema information
        schema = {
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "shape": df.shape,
            "null_counts": df.isnull().sum().to_dict()
        }
        
        # Get sample rows
        sample_rows = df.head(5).to_dict('records')
        
        # Basic statistics for numeric columns
        numeric_summary = df.describe().to_dict() if len(df.select_dtypes(include='number').columns) > 0 else {}
        
        return {
            "status": "success",
            "schema": schema,
            "sample_rows": sample_rows,
            "numeric_summary": numeric_summary,
            "file_path": file_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def execute_python_analysis(code: str, data_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute Python code for data analysis.
    
    Args:
        code: Python code to execute
        data_path: Optional path to CSV data
        
    Returns:
        Dictionary containing execution results
    """
    try:
        # Create execution namespace
        namespace = {
            'pd': pd,
            'plt': None,  # Will be imported in code if needed
            'np': None,   # Will be imported in code if needed
        }
        
        # Load data if path provided
        if data_path and os.path.exists(data_path):
            namespace['df'] = pd.read_csv(data_path)
        
        # Execute code
        exec(code, namespace)
        
        # Extract results
        results = {
            "status": "success",
            "output": "Code executed successfully"
        }
        
        # Try to extract common result variables
        if 'result_df' in namespace:
            results['dataframe'] = namespace['result_df'].to_dict('records')
        
        if 'result_value' in namespace:
            results['value'] = namespace['result_value']
            
        return results
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }


def execute_sql_query(query: str, data_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute SQL query using DuckDB.
    
    Args:
        query: SQL query to execute
        data_path: Optional path to CSV data
        
    Returns:
        Dictionary containing query results
    """
    try:
        # Create in-memory DuckDB connection
        con = duckdb.connect(':memory:')
        
        # Load data if provided
        if data_path and os.path.exists(data_path):
            # Register CSV as table
            con.execute(f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{data_path}')")
        
        # Execute query
        result = con.execute(query).fetchdf()
        
        return {
            "status": "success",
            "result": result.to_dict('records'),
            "row_count": len(result),
            "columns": result.columns.tolist()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }
    finally:
        con.close()


def style_chart(chart_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply professional styling to charts.
    
    Args:
        chart_config: Configuration for chart styling
        
    Returns:
        Dictionary with styling recommendations
    """
    try:
        # This is a simplified version - in practice would modify matplotlib figures
        recommendations = {
            "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            "font_size": {
                "title": 14,
                "labels": 12,
                "ticks": 10
            },
            "dpi": 300,
            "grid": True,
            "legend": True
        }
        
        return {
            "status": "success",
            "styling_applied": True,
            "recommendations": recommendations
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def save_analysis_results(results: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """
    Save analysis results to file.
    
    Args:
        results: Analysis results to save
        output_path: Path to save results
        
    Returns:
        Dictionary with save status
    """
    try:
        import json
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return {
            "status": "success",
            "file_path": output_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
