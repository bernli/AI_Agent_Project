## Project Overview - InsightLoop

NOTE: This project was developed for the [Kaggle Agents Intensive Capstone project](https://www.kaggle.com/competitions/agents-intensive-course-capstone-2025/).

This project contains the core logic for InsightLoop, a multi-agent data analysis system designed to transform business questions into actionable insights. The agent is built using Google Agent Development Kit (ADK) and follows a modular architecture.

![Architecture](./thumbnail.png "InsightLoop Architecture")

### Problem Statement

Business teams need fast answers to make informed decisions, but getting insights from data is painfully slow. A product manager asking "Which customer segments are driving our Q4 revenue growth?" faces a typical 48-hour wait for the analytics team to respond. Even simple questions require submitting data request tickets, waiting for analyst availability, receiving initial results, requesting corrections, and waiting again. This creates a critical bottleneck where decisions are delayed by days, opportunities are missed, and momentum is lost. For non-technical business users who can't write SQL or Python themselves, data exploration becomes completely inaccessible. The repetitive nature of manual analysis—loading CSVs, inspecting schemas, writing queries, debugging errors, generating visualizations—drains analyst productivity and prevents them from focusing on high-value strategic work. The problem isn't lack of data; it's the 48-hour barrier between question and insight that kills business agility.

### Solution Statement

InsightLoop automates the complete data analysis workflow through intelligent agent coordination. When a business user asks a question in natural language, the system automatically researches the dataset schema, generates a comprehensive analysis plan, executes real pandas code and SQL queries in parallel for validation, produces publication-ready styled visualizations, and delivers plain-English business insights—all in approximately 30 seconds. The agents work together to transform raw tabular data from CSV files and SQL databases into professional KPI dashboards and actionable recommendations, eliminating the need for technical skills or analyst bottlenecks. By maintaining conversation context through session memory, InsightLoop supports iterative exploration where users can refine their analysis with follow-up questions, dramatically accelerating the path from curiosity to confident decision-making.

### Architecture

Core to InsightLoop is the `data_analyst_agent`—a prime example of a multi-agent system. It's not a monolithic application but an ecosystem of specialized agents, each contributing to a different stage of the data analysis process. This modular approach, facilitated by Google's Agent Development Kit, allows for a sophisticated and robust workflow. The central orchestrator of this system is the `interactive_analyst_agent`.

![Architecture](./flow_adk_web.png "InsightLoop Agent Flow")

The `interactive_analyst_agent` is constructed using the `Agent` class from the Google ADK. Its definition highlights several key parameters: the `name`, the `model` it uses for its reasoning capabilities, and a detailed `description` and `instruction` set that governs its behavior. Crucially, it also defines the `sub_agents` it can delegate tasks to and the `tools` it has at its disposal.

The real power of the `data_analyst_agent` lies in its team of specialized sub-agents, each an expert in its domain.

**Strategic Planner: `robust_analysis_planner`**

This agent is responsible for creating a well-structured and comprehensive analysis plan based on the user's business question. It analyzes the dataset schema (columns, data types, sample rows) and determines the required transformations, filters, aggregations, and visualizations needed to answer the question. To ensure high-quality output, it's implemented as a `LoopAgent`, a pattern that allows for retries and validation. The `PlanValidationChecker` ensures that the generated plan is executable and addresses the user's intent.

**Python Data Scientist: `robust_python_executor`**

Once the analysis plan is approved, the `robust_python_executor` takes over. This agent is an expert data scientist, capable of executing complex pandas transformations, statistical calculations, and matplotlib visualizations. It uses the approved plan to generate and execute Python code, with a strong emphasis on data quality and error handling. Like the planner, it's a `LoopAgent` that uses a `PythonOutputValidationChecker` to ensure the code executes successfully and produces valid results.

**SQL Analyst: `sql_executor`**

Running in parallel with the Python executor, the `sql_executor` translates the analysis plan into optimized SQL queries. This agent executes queries against an in-memory DuckDB database, performing the same analysis independently. This dual-execution strategy provides cross-validation of results, significantly improving reliability and catching potential errors before they reach the user.

**Visualization Designer: `chart_styler`**

After the data analysis is complete, the `chart_styler` transforms raw matplotlib figures into publication-ready visualizations. This agent is a `LoopAgent` that applies corporate styling, consistent color palettes, clear axis labels, number formatting, and anomaly highlighting. It iterates until quality checks pass, ensuring every chart meets professional standards.

**Business Translator: `insight_reviewer`**

The `insight_reviewer` is the final agent in the pipeline, responsible for translating technical results into business language. It cross-validates Python and SQL outputs, identifies patterns and anomalies, generates plain-English summaries, and provides actionable recommendations. This agent ensures that non-technical users receive insights they can immediately understand and act upon.

### Essential Tools and Utilities

The `data_analyst_agent` and its sub-agents are equipped with a variety of tools to perform their tasks effectively.

**CSV Data Loader (`load_csv_data`)**

A fundamental tool that ingests user-provided CSV files, parses schemas and data types, extracts sample rows for context, and handles encoding issues. This tool provides the raw material for all subsequent analysis.

**Python Code Execution (`execute_python_analysis`)**

This tool runs pandas, numpy, and matplotlib code in a secure sandbox environment. It returns DataFrames, figures, descriptive statistics, and execution logs. Error handling ensures that code failures are captured and reported clearly, enabling the validation loop to retry with corrections.

**SQL Query Engine (`execute_sql_query`)**

An in-memory DuckDB database engine that executes SQL queries with support for complex operations like GROUP BY, window functions, and CTEs. Results are returned in tabular format for comparison with Python outputs, providing the foundation for cross-validation.

**Chart Styling Tool (`style_chart`)**

This tool automatically enhances matplotlib figures by applying consistent formatting, color schemes, and annotations. It supports the `LoopAgent` pattern by returning quality scores, enabling iterative improvement until visualizations meet professional standards.

**Validation Checkers (`PlanValidationChecker`, `PythonOutputValidationChecker`, `ChartQualityChecker`)**

These custom `BaseAgent` implementations are a key part of the system's robustness. They check for the completeness and correctness of analysis plans, Python execution results, and chart quality, respectively. If validation fails, they do nothing, causing the `LoopAgent` to retry. If validation succeeds, they escalate with `EventActions(escalate=True)`, which signals to the `LoopAgent` that it can proceed. This is a powerful mechanism for ensuring quality and controlling the flow of execution in a multi-agent system.

### Sessions & Memory

InsightLoop uses ADK session management to maintain conversation context across multiple queries. The system remembers previously loaded datasets, applied filters, analysis history, and user preferences (chart styles, output formats). This enables natural follow-up questions like "Now show only premium customers" or "Compare to last year," where the agent understands the ongoing context without requiring users to repeat information.

### Observability

The system leverages ADK's built-in logging and tracing capabilities to monitor agent execution, track tool calls, compare Python vs. SQL results, and identify performance bottlenecks. This observability layer is crucial for debugging, improving agent prompts, and ensuring reliability in production environments.

### Conclusion

The beauty of the `data_analyst_agent` lies in its coordinated workflow. The `interactive_analyst_agent` acts as a project manager, orchestrating the efforts of its specialized team. It delegates planning to the strategic planner, executes analysis through parallel Python and SQL engines, validates results through cross-checking, enhances visualizations through the chart styler, and delivers business insights through the translator agent. This multi-agent coordination, powered by the Google ADK, results in a system that is modular, reusable, and scalable.

InsightLoop is a compelling demonstration of how multi-agent systems, built with powerful frameworks like Google's Agent Development Kit, can tackle complex, real-world business intelligence problems. By breaking down the process of data analysis into a series of manageable tasks and assigning them to specialized agents, it creates a workflow that is both efficient and robust—transforming a 48-hour analyst bottleneck into a 30-second self-service experience.

### Value Statement

InsightLoop reduced my data analysis time from 48 hours (waiting for analysts) to 30 seconds, enabling me to make faster business decisions with higher confidence. The dual validation approach (Python + SQL) eliminated manual errors that previously required time-consuming corrections. I've also been able to explore data across new business domains—the agent handles complex SQL queries and statistical analysis that I wouldn't be able to do myself given time constraints and technical expertise gaps.

If I had more time I would add additional agents for automatic anomaly detection, forecasting, and A/B test analysis. I would also integrate enterprise data warehouse connectors (BigQuery, Snowflake) and build a KPI monitoring agent that proactively alerts when metrics deviate from expected ranges. This would require integrating applicable MCP servers or building custom database connection tools.

## Installation

This project was built against Python 3.11.3.

It is suggested you create a virtual environment using your preferred tooling e.g. uv.

Install dependencies e.g. pip install -r requirements.txt

### Running the Agent in ADK Web mode

From the command line of the working directory execute the following command:

```bash
adk web
```

**Run the integration test:**

```bash
python -m tests.test_agent
```

## Project Structure

The project is organized as follows:

*   `insight_loop/`: The main Python package for the agent.
    *   `agent.py`: Defines the main `interactive_analyst_agent` and orchestrates the sub-agents.
    *   `sub_agents/`: Contains the individual sub-agents, each responsible for a specific task.
        *   `analysis_planner.py`: Generates the analysis plan.
        *   `python_executor.py`: Executes pandas/matplotlib code.
        *   `sql_executor.py`: Executes SQL queries.
        *   `chart_styler.py`: Styles visualizations.
        *   `insight_reviewer.py`: Translates results to business language.
    *   `tools.py`: Defines the custom tools used by the agents.
    *   `config.py`: Contains the configuration for the agents, such as the models to use.
*   `eval/`: Contains the evaluation framework for the agent.
*   `tests/`: Contains integration tests for the agent.

## Workflow

The `interactive_analyst_agent` follows this workflow:

1.  **Load Data:** The user uploads a CSV file or provides SQL database connection details. The agent loads the data using the `load_csv_data` or database connector tool.
2.  **Ask Question:** The user asks a business question in natural language (e.g., "Which regions had the strongest revenue growth last quarter?").
3.  **Plan Analysis:** The agent delegates the task of generating an analysis plan to the `robust_analysis_planner`, which examines the dataset schema and creates a structured execution plan.
4.  **Execute in Parallel:** The agent simultaneously delegates execution to both `robust_python_executor` (pandas/matplotlib) and `sql_executor` (DuckDB), ensuring dual validation of results.
5.  **Style Visualizations:** Raw charts are sent to the `chart_styler` agent, which iteratively applies professional formatting until quality standards are met.
6.  **Generate Insights:** The `insight_reviewer` cross-validates Python and SQL results, identifies patterns, and translates findings into plain-English business recommendations.
7.  **Present Results:** The agent presents styled charts and business insights to the user.
8.  **Follow-up Questions:** The user can ask follow-up questions (e.g., "Show only premium customers"), and the agent uses session memory to maintain context and refine the analysis.
9.  **Export (Optional):** The user can request to export the analysis results, charts, and insights to files for presentation or reporting purposes.
