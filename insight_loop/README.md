# InsightLoop - AI-Powered Business Intelligence Agent

**Turn business questions into actionable insights in 30 seconds.**

Built with Google Agent Development Kit (ADK) and Gemini 2.5 Flash.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** 
- **pip** package manager
- **Gemini API Key** from Google AI Studio

### Installation

#### 1. Create Virtual Environment

```bash
python -m venv .venv

# Activate
# macOS/Linux:
source .venv/bin/activate

# Windows CMD:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Get Gemini API Key

1. Go to **https://aistudio.google.com/apikey**
2. Click **"Create API Key"**
3. Copy the key (starts with "AIza...")

#### 4. Configure API Key

Open the `.env` file and replace:

```bash
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

With your actual key:

```bash
GOOGLE_API_KEY=AIza...your_actual_key
```

**IMPORTANT**: Never commit `.env` to Git!

---

## 🎯 Running InsightLoop

```bash
# Navigate to PARENT directory of insight_loop/
cd /path/to/parent/

# Start ADK web interface
adk web
```

Open browser to **http://localhost:8000**

---

## 🏗️ Architecture

### Multi-Agent System with 5 Specialized Agents:

```
Root Agent (LlmAgent)
├── Analysis Planner (LoopAgent)
├── Python Executor (LoopAgent)
├── SQL Executor (Agent)
├── Chart Styler (LoopAgent)
└── Insight Reviewer (Agent)
```

### Agent Details:

#### 1. **Root Agent** - `LlmAgent`
- Main orchestrator
- Coordinates all sub-agents
- Manages conversation flow

#### 2. **Analysis Planner** - `LoopAgent`
- Creates structured analysis plans
- Validates plan quality
- Retries if plan incomplete (max 3x)

#### 3. **Python Executor** - `LoopAgent`
- Executes pandas/matplotlib code
- Validates execution success
- Retries on errors (max 3x)

#### 4. **SQL Executor** - Standard `Agent`
- Runs DuckDB SQL queries
- Cross-validates with Python results
- No retry needed (simpler)

#### 5. **Chart Styler** - `LoopAgent`
- Applies professional styling
- Validates quality score
- Iterates until quality ≥ threshold

#### 6. **Insight Reviewer** - Standard `Agent`
- Translates to business language
- Cross-validates results
- Generates recommendations

---

## 📊 Project Structure

```
insight_loop/
├── agent.py                    # Main orchestrator (LlmAgent)
├── config.py                   # Model configuration
├── tools.py                    # Custom tools
├── .env                        # API keys (DO NOT COMMIT!)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Dependencies
├── sub_agents/
│   ├── analysis_planner.py    # LoopAgent with validator
│   ├── python_executor.py     # LoopAgent with validator
│   ├── sql_executor.py        # Standard Agent
│   ├── chart_styler.py        # LoopAgent with validator
│   └── insight_reviewer.py    # Standard Agent
└── tests/
    └── test_agent.py          # Integration tests
```

---

## 🔧 ADK Concepts Demonstrated

✅ **Multi-Agent Systems**
- Main orchestrator: `LlmAgent`
- Sub-agents with different types

✅ **Agent Types**
- `LlmAgent`: Root orchestrator
- `LoopAgent`: Planner, Python Executor, Chart Styler (with retry logic)
- Standard `Agent`: SQL Executor, Insight Reviewer

✅ **Custom Tools**
- `load_csv_data`
- `execute_python_analysis`
- `execute_sql_query`
- `style_chart`
- `save_analysis_results`

✅ **Validators** (for LoopAgents)
- `PlanValidationChecker`
- `PythonOutputValidationChecker`
- `ChartQualityChecker`

✅ **Sessions & Memory**
- State management
- Conversation context

✅ **Observability**
- ADK built-in logging
- Tracing and metrics

---

## 🔑 API Key Configuration

### Location
API key is stored in `.env` file:

```bash
GOOGLE_API_KEY=AIza...your_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### How ADK Loads It
ADK automatically loads `.env` file from project root. No additional code needed!

### Security
- ✅ `.env` is in `.gitignore`
- ❌ Never commit to Git
- ❌ Never hardcode in source

---

## 🎓 Model Configuration

Models are configured in `config.py`:

```python
MAIN_AGENT_MODEL = "gemini-2.5-flash"
PLANNER_MODEL = "gemini-2.5-flash"
# etc.
```

Available models:
- `gemini-2.5-flash` (recommended, stable)
- `gemini-2.0-flash-exp` (experimental, latest features)
- `gemini-1.5-pro` (more powerful, slower)

---

## 🧪 Testing

```bash
python -m tests.test_agent
```

---

## 📚 Resources

- [ADK Documentation](https://google.github.io/adk-docs)
- [Google AI Studio](https://aistudio.google.com)
- [ADK GitHub](https://github.com/google/adk-python)

---

## 📄 License

MIT License

---

**Built for Agents Intensive Capstone Project**
