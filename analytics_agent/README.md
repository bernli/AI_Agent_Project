# Analytics Agent - AI-Powered Business Intelligence Agent

Turn business questions into Python-based insights fast. Built with Google Agent Development Kit (ADK) and Gemini 2.5.

---

## Quick Start

1) Install deps
```bash
python -m venv .venv
# Activate env, then:
pip install -r requirements.txt
```

2) Configure API key  
Create `.env` in project root with:
```
GOOGLE_API_KEY=AIza...your_key_here
```

3) Run ADK web UI
```bash
adk web
# open http://localhost:8000
```

---

## Architecture (Current)

- `agent.py`: root `Agent` orchestrating the flow.
- `sub_agents/code_review_loop.py`: `LoopAgent` that writes code (`code_writer_agent`), runs safety checks, and validates output.
- `sub_agents/validation_checkers.py`: safety/validation helpers.
- `tools.py`: analysis tools (`analyze_dataframe`, `execute_python_analysis`, chart styling, CSV helpers).
- `config.py`: model and retry configuration.
- `test_agent_load.py`, `test_imports.py`: sanity checks for imports and agent wiring.

SQL/DuckDB is intentionally removed for now.

---

## Usage Flow
1. Call `analyze_dataframe(file_path)` to load schema/stats/context.
2. Ask your question; the loop writes/reviews code until safe.
3. Call `execute_python_analysis` with the generated code and CSV path.
4. Receive results (`result_value` or `result_df`) and any charts saved to `charts/`.

---

## Testing
```bash
python -m analytics_agent.test_agent_load
python -m analytics_agent.test_imports
```

---

## Notes
- Never commit `.env`.
- Generated code must write to `result_value` (scalar) or `result_df` (DataFrame); charts are auto-saved with professional styling.
