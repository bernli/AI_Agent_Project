"""Custom tools for InsightLoop agents."""

import os
import re
import pandas as pd
import numpy as np
import io
from typing import Dict, Any, Optional
from .config import DISALLOWED_PATTERNS


def _convert_to_native(obj):
    """Convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: _convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_to_native(v) for v in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    return obj


def analyze_dataframe(file_path: str) -> dict:
    """Analyzes a CSV file and returns complete context for code generation."""
    if not os.path.exists(file_path):
        return {"status": "error", "error": f"File not found: {file_path}"}

    df = pd.read_csv(file_path)

    # Get unique values for categorical columns
    unique_values = {}
    for col in df.columns:
        if df[col].dtype == 'object' or 'date' in col.lower():
            vals = df[col].unique()
            if len(vals) <= 20:
                unique_values[col] = sorted(vals.tolist())
            else:
                unique_values[col] = {
                    "count": len(vals),
                    "first": sorted(vals.tolist())[:5],
                    "last": sorted(vals.tolist())[-5:]
                }

    return _convert_to_native({
        "status": "success",
        "file_path": file_path,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "shape": list(df.shape),
        "unique_values": unique_values,
        "sample_data": df.head(5).to_dict('records'),
        "statistics": df.describe().to_dict()
    })


def execute_python_analysis(
    code: str,
    data_path: Optional[str] = None,
    timeout_seconds: int = 30
) -> Dict[str, Any]:
    """
    Execute Python code for data analysis with timeout protection.

    Args:
        code: Python code to execute
        data_path: Optional path to CSV data file
        timeout_seconds: Maximum execution time in seconds (default: 30)

    Returns:
        Dictionary containing execution results
    """
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    import signal
    from contextlib import contextmanager

    @contextmanager
    def timeout(seconds):
        """Context manager for timeout protection."""
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Code execution exceeded {seconds} seconds timeout")

        # Set the signal handler and alarm
        if hasattr(signal, 'SIGALRM'):  # Unix/Linux/Mac only
            original_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                yield
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, original_handler)
        else:
            # Windows doesn't support SIGALRM, use threading instead
            import threading
            timer = threading.Timer(seconds, lambda: (_ for _ in ()).throw(TimeoutError(f"Code execution exceeded {seconds} seconds timeout")))
            timer.start()
            try:
                yield
            finally:
                timer.cancel()

    # Security check: validate code against disallowed patterns
    lowered_code = code.lower()
    if any(pat in lowered_code for pat in DISALLOWED_PATTERNS):
        return {
            "status": "error",
            "error_message": "Generated code contains disallowed operations. Please revise and try again.",
            "error_type": "SafetyCheckError"
        }

    # Validate data_path before execution
    if not data_path:
        return {
            "status": "error",
            "error_message": "data_path is required. Please provide the path to the CSV file.",
            "error_type": "ValueError"
        }

    if not os.path.exists(data_path):
        return {
            "status": "error",
            "error_message": f"File not found: {data_path}. Please provide a valid file path.",
            "error_type": "FileNotFoundError"
        }

    try:
        import contextlib
        import io as string_io

        # Strip FILE_PATH marker lines from executable code
        executable_code = "\n".join(
            line for line in code.splitlines()
            if not line.strip().lower().startswith("file_path")
        )

        # Create execution namespace
        namespace = {
            'pd': pd,
            'plt': plt,
            'np': np,
            'io': io,
            'os': os
        }

        # Load data from CSV
        namespace['df'] = pd.read_csv(data_path)

        # Capture stdout/stderr to aid debugging and execute with timeout protection
        stdout_buffer = string_io.StringIO()
        stderr_buffer = string_io.StringIO()
        with timeout(timeout_seconds):
            with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                exec(executable_code, namespace)

        # Extract results
        results = {
            "status": "success",
            "output": "Code executed successfully"
        }

        # Extract DataFrames
        if 'result_df' in namespace:
            results['dataframe'] = namespace['result_df'].to_dict('records')

        # Extract scalar values
        if 'result_value' in namespace:
            results['value'] = namespace['result_value']

        stdout_value = stdout_buffer.getvalue().strip()
        stderr_value = stderr_buffer.getvalue().strip()
        if stdout_value:
            results["stdout"] = stdout_value
        if stderr_value:
            results["stderr"] = stderr_value

        return _convert_to_native(results)

    except TimeoutError as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": "TimeoutError"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }


def save_csv_string_to_file(csv_content: str, file_name: str = "temp_data.csv") -> Dict[str, Any]:
    """
    Save CSV string content to a file in the current directory.

    Args:
        csv_content: CSV data as string
        file_name: Name of the file (default: "temp_data.csv")

    Returns:
        Dictionary with absolute file path
    """
    try:
        # Security: Validate filename to prevent path traversal
        if ".." in file_name or "/" in file_name or "\\" in file_name or ":" in file_name:
            return {
                "status": "error",
                "error_message": "Invalid file name: path separators and '..' are not allowed"
            }

        # Only allow safe characters in filename
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', file_name):
            return {
                "status": "error",
                "error_message": "Invalid file name: only alphanumeric, underscore, hyphen, and dot are allowed"
            }

        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(data_dir, exist_ok=True)

        # Create absolute path
        file_path = os.path.join(data_dir, file_name)

        # Additional security: ensure resolved path is still within data_dir
        if not os.path.abspath(file_path).startswith(os.path.abspath(data_dir)):
            return {
                "status": "error",
                "error_message": "Invalid file path: must be within data directory"
            }

        # Save CSV content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        # Verify file was created
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "error_message": f"Failed to create file at {file_path}"
            }

        return {
            "status": "success",
            "file_path": file_path,
            "message": f"CSV content saved to {file_path}"
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
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
