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


def _apply_professional_styling():
    """
    Apply professional styling to all current matplotlib figures.
    Uses the style_chart configuration.
    """
    import matplotlib.pyplot as plt

    # Get styling configuration
    style_config = style_chart()['style_config']

    # Apply to all current figures
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        ax = fig.gca()

        # Apply grid
        if style_config['grid']['enabled']:
            ax.grid(
                alpha=style_config['grid']['alpha'],
                color=style_config['grid']['color'],
                linestyle=style_config['grid']['linestyle']
            )

        # Apply axes styling
        ax.set_facecolor(style_config['axes']['facecolor'])
        for spine in ax.spines.values():
            spine.set_edgecolor(style_config['axes']['edgecolor'])
            spine.set_linewidth(style_config['axes']['linewidth'])

        # Apply font styling to existing labels
        if ax.get_title():
            ax.title.set_fontsize(style_config['fonts']['title']['size'])
            ax.title.set_fontweight(style_config['fonts']['title']['weight'])

        if ax.get_xlabel():
            ax.xaxis.label.set_fontsize(style_config['fonts']['labels']['size'])

        if ax.get_ylabel():
            ax.yaxis.label.set_fontsize(style_config['fonts']['labels']['size'])

        ax.tick_params(labelsize=style_config['fonts']['ticks']['size'])

        # Apply legend styling if legend exists
        legend = ax.get_legend()
        if legend:
            legend.set_frame_on(True)
            legend.get_frame().set_alpha(style_config['legend']['framealpha'])


def _save_matplotlib_charts() -> Dict[str, Any]:
    """
    Save all matplotlib figures to files and as base64 encoded data.

    Returns:
        Dictionary with file paths and base64 encoded chart data
    """
    import matplotlib.pyplot as plt
    import base64
    from io import BytesIO

    # Apply professional styling before saving
    _apply_professional_styling()

    saved_charts = []
    chart_data_list = []
    charts_dir = "charts"
    os.makedirs(charts_dir, exist_ok=True)

    for i, fig_num in enumerate(plt.get_fignums()):
        fig = plt.figure(fig_num)
        chart_path = os.path.join(charts_dir, f"chart_{i+1}.png")

        # Save to file
        fig.savefig(chart_path, format='png', dpi=300, bbox_inches='tight')
        saved_charts.append(chart_path)

        # Also save as base64 for inline display
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        chart_data_list.append({
            'filename': f"chart_{i+1}.png",
            'data': chart_base64,
            'mime_type': 'image/png'
        })
        buffer.close()

        plt.close(fig)

    return {
        'file_paths': saved_charts,
        'chart_data': chart_data_list
    }


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

        # Save any matplotlib charts that were created
        chart_results = _save_matplotlib_charts()
        if chart_results['file_paths']:
            results['charts'] = chart_results['file_paths']
            results['chart_data'] = chart_results['chart_data']
            results['output'] = f"Code executed successfully. Created {len(chart_results['file_paths'])} chart(s)."

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


def style_chart(figure_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Apply standard professional styling to matplotlib charts.

    Args:
        figure_path: Optional path to saved matplotlib figure

    Returns:
        Dictionary with standard styling configuration applied
    """
    # Standard professional styling configuration
    standard_style = {
        "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
        "fonts": {
            "title": {"size": 14, "weight": "bold", "family": "sans-serif"},
            "labels": {"size": 12, "family": "sans-serif"},
            "ticks": {"size": 10}
        },
        "grid": {
            "enabled": True,
            "alpha": 0.3,
            "color": "#cccccc",
            "linestyle": "--"
        },
        "figure": {
            "dpi": 300,
            "size": (10, 6),
            "facecolor": "white"
        },
        "legend": {
            "enabled": True,
            "location": "best",
            "framealpha": 0.9
        },
        "axes": {
            "facecolor": "white",
            "edgecolor": "#333333",
            "linewidth": 1.2
        }
    }

    return {
        "status": "success",
        "styling_applied": True,
        "style_config": standard_style,
        "message": "Standard professional styling configuration ready to apply"
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
