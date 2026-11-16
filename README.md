# CareCompanion: Agentic Health Coach with Persistent Memory

CareCompanion is an AI wellness coach that **remembers user history across multiple sessions** and **adapts its advice** based on tracked biometric outcomes.

Built for the problem statement:
> *"Build a coaching agent that remembers a user's history across multiple sessions and adjusts its advice based on past interactions... demo showing advice changing across 2-3 simulated sessions."*

---

## 🌟 Key Features

1. **Agentic Tool Loop:**
   * Powered by Groq / Azure OpenAI with autonomous tool calling.
   * Tools include: `get_user_profile`, `recall_memories`, `get_health_summary`, `check_advice_outcomes`, and `log_advice`.
2. **Persistent Long-Term Memory (SQLite):**
   * Stores goals, injuries/constraints, preferences, and session reflection summaries across sessions in `data/carecompanion.db`.
3. **Outcome-Driven Strategy Adaptation:**
   * When advice is given, a baseline is recorded (e.g. 3,500 steps/day).
   * In future sessions, the agent compares recent biometric averages against the baseline (`improved`, `no_change`, `worse`).
   * If a strategy stalls or fails, the coach **changes tactics** instead of repeating ineffective advice.
4. **Dynamic User Creation ("➕ Add New User"):**
   * Create custom users live from the sidebar.
   * Generates realistic baseline biometric data tailored to the chosen goal (Steps, Sleep, Cardio).
   * Automatically conducts an interactive onboarding session, records constraints, and links past memory in follow-up sessions.
5. **Safety Guardrails:**
   * Red-flag symptom detection (e.g. chest pain, shortness of breath) immediately directs users to emergency medical care. The agent never provides clinical medical diagnoses.
6. **Zero-Setup Offline Mock Mode:**
   * Operates completely offline with built-in rule-based coaching if no API key is provided.

---

## 📁 Project Layout

```
carecompanion/
├── app.py                 # Interactive Streamlit Web UI (Chat, Memory inspector, Charts)
├── demo.py                # Headless CLI demo comparing Memory ON vs. OFF
├── seed_demo_data.py      # Seeds 3 pre-populated benchmark personas into SQLite
├── check_connection.py    # Validates LLM connectivity and tool-calling capabilities
├── generate_data.py       # Recreates synthetic 4-week Fitbit datasets
├── requirements.txt       # Project dependencies
├── .env.example           # Environment template (API keys, model configuration)
├── .gitignore             # Git ignore rules (secrets, venv, databases)
├── carecompanion/
│   ├── agent.py           # Core agent loop and execution flow
│   ├── tools.py           # Tool definitions and execution schemas
│   ├── memory.py          # Memory storage and semantic keyword retrieval
│   ├── db.py              # SQLite database schema and query helpers
│   ├── reflection.py      # End-of-session reflection and durable fact extraction
│   ├── safety.py          # Red-flag medical symptom triage and disclaimers
│   ├── llm.py             # OpenAI-compatible LLM client (Groq / Azure OpenAI)
│   ├── mock_llm.py        # Rule-based offline LLM fallback
│   ├── data_loader.py     # Fitbit dataset loader (synthetic CSVs / PMData)
│   └── synthetic.py       # Synthetic health data generation
├── tests/
│   └── test_all.py        # Offline unit and integration test suite
└── data/
    └── synthetic/         # Baseline biometric data (steps, sleep, heart rate, calories)
```

---

## 🚀 Quick Setup Guide

### 1. Prerequisites
* **Python 3.10+** installed ([python.org](https://python.org/)). Ensure *"Add Python to PATH"* is checked.

### 2. Environment Setup
In your terminal, navigate to the project directory:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file from the provided template:

```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```

Open `.env` and set your preferred provider:

* **Using Groq (Recommended - Free & Fast):**
  1. Get a free API key at [console.groq.com/keys](https://console.groq.com/keys).
  2. Configure in `.env`:
     ```env
     LLM_PROVIDER=groq
     GROQ_API_KEY=your_groq_api_key_here
     GROQ_MODEL=qwen/qwen3.8-27b
     ```
     *(Note: You can also use `llama-3.3-70b-versatile` if supported on your account tier).*

* **Using Offline Mock Mode (No API Key Required):**
  ```env
  LLM_PROVIDER=mock
  ```

### 4. Verify Connection
```bash
python check_connection.py
```
*(Should output `OK: connection works and the model can call tools`)*.

---

## 🏃 Running the Application

### Option A: Interactive Streamlit Web UI
Launch the interactive browser application:

```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501** (or port 8502).

**What to try:**
1. **Pre-populated Personas:** Select **Meera (p02)** or **Rohan (p03)** to inspect their saved memories and outcome tracking.
2. **Dynamic Onboarding:** Open the **"➕ Add New User"** expander in the sidebar, create a new profile (e.g. *Alex*), and test Session 1 onboarding and Session 2 memory recall.
3. **Memory ON vs. OFF:** Toggle the **"Memory ON"** switch in the sidebar to compare personalized coaching against generic advice.

### Option B: Pre-populating Demo Data
To quickly restore or pre-populate the 3 benchmark demo personas (Aarav, Meera, Rohan) with 3 full sessions of historical data:

```bash
python seed_demo_data.py
```

### Option C: Headless Comparative Report (CLI)
Run a simulated multi-session evaluation comparing Memory ON vs. Memory OFF:

```bash
python demo.py --user p02
```
* Generates a side-by-side Markdown report under `demo_output/report_p02.md`.

---

## 🧪 Running Automated Tests

Run the test suite to verify all core components offline:

```bash
python -m pytest -q
```
* **Expected result:** `8 passed in ~1s` (100% passing).

---

## 🗄️ Database Architecture

CareCompanion uses a local SQLite database (`data/carecompanion.db`) with five core tables:

* `users`: `id`, `name`
* `sessions`: `id`, `user_id`, `session_no`, `sim_date`, `started`, `ended`, `summary`
* `messages`: `id`, `session_id`, `role`, `content`, `created`
* `memories`: `id`, `user_id`, `session_id`, `session_no`, `category`, `content`, `importance`, `created`
* `advice`: `id`, `user_id`, `session_id`, `session_no`, `text`, `metric`, `direction`, `target`, `baseline`, `status`, `current`, `change_pct`, `outcome_session_no`
