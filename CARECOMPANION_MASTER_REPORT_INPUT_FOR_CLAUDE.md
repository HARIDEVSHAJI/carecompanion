# CARECOMPANION: MASTER TECHNICAL SPECIFICATION & COMPREHENSIVE REPORT KNOWLEDGE BASE
## Complete Reference for Generating a 20–25 Page Academic Project Report with Visual Figures and Zero AI Plagiarism

---

> ### 🛑 STRICT OPERATIONAL INSTRUCTIONS FOR CLAUDE:
> 
> You are acting as the primary author and technical compiler for the official academic capstone project report on **CareCompanion**.
> 
> **CRITICAL REPORT SPECIFICATIONS:**
> 1. **Target Report Length:** Exactly **20 to 25 pages** of dense, professional academic engineering prose (equivalent to 8,000–10,500 words with 16 visual figures, 20+ structured tables, code walkthroughs, dialogue transcripts, and mathematical proofs).
> 2. **Reference Structure:** Follow the exact layout, section numbering, and presentation hand-overs of the reference *FloatChat* report:
>    - **Cover & Metadata:** Title, meta table, two-student authorship matrix, formal Table of Contents with dot leaders.
>    - **Executive Summary & Abstract:** Abstract with 4-card KPI metric banner, team work division diagram, and originality statement.
>    - **Part I — Problem Context, Clinical Foundations & Solution Concept:** (Lead Author: **Haridev Shaji**, Reg. No. **12313476**, Slides 1–4).
>    - **Part II — System Architecture, Database & Agent Reasoning:** (Joint Authors: **Haridev Shaji** & **Nikhil Singh**, Reg. No. **12323695**, Slides 5–7).
>    - **Part III — Implementation, Verification, Empirical Results & Future Scope:** (Lead Author: **Nikhil Singh**, Reg. No. **12323695**, Slides 8–10).
>    - **References & Formal Appendices:** Appendices A, B, C, D, and E.
> 3. **Image & Figure Generation Requirement (16 FIGURES TOTAL):**
>    - You must include and generate **all 16 technical figures** specified in Section 5 of this document.
>    - For conceptual diagrams and architectures, generate clean, copy-pasteable **SVG vector code** or **Mermaid diagrams** (`flowchart TD`, `sequenceDiagram`, `erDiagram`).
>    - For data charts, biometrics, and test statistics, provide both the ASCII/SVG visual rendering AND the complete, executable **Python Matplotlib script** so the user can render high-resolution PNGs directly.
> 4. **Strict Anti-AI Plagiarism & Human Writing Guidelines:**
>    - **Zero AI Buzzwords:** Completely avoid generic AI clichés: *"in today's fast-paced world"*, *"delve into"*, *"testament to"*, *"tapestry"*, *"beacon"*, *"fostering"*, *"harnessing"*, *"paradigm shift"*, *"game-changer"*, *"crucial role"*, *"moreover"*, *"furthermore"*, *"in conclusion"*.
>    - **Human Engineering Voice:** Write like an experienced software engineer and computer science researcher. Use high burstiness (mix concise, punchy technical sentences with detailed analytical paragraphs). Discuss concrete bugs encountered during development (Groq HTTP 404, Qwen tool token leaks, fallback assertion breaks), quantitative tradeoffs, and empirical numbers.
>    - **Zero Hallucination:** Every number, tool name, SQL schema, test count (8/8 passing in 0.77s), and persona detail must come strictly from this document. Do not invent external frameworks or non-existent features.

---

# SECTION 1: PROJECT METADATA & TEAM WORK DIVISION

## 1.1 Academic Meta Table

| Specification Parameter | Document Value |
| :--- | :--- |
| **Project Title** | CareCompanion: An Agentic Healthcare Coaching System with Persistent Cross-Session Memory, Longitudinal Biometric Outcome Tracking, and Deterministic Safety Guardrails |
| **Course Reference** | LLM & Agentic AI (CA1 Capstone Project-Based Assignment, 2026–2027) |
| **Institutional Affiliation** | School of Computer Science & Engineering, Lovely Professional University, Punjab, India |
| **Problem Statement Reference**| Problem Statement #4: Autonomous Coaching Agent with Persistent Memory & Adaptive Outcome Progression |
| **Official Repository** | `https://github.com/HARIDEVSHAJI/carecompanion.git` (Branch `main`, clean working tree) |
| **Distribution Package** | `carecompanion_deploy.zip` (~39 KB clean package, zero virtual environments, zero secrets) |
| **Date of Submission** | November 2026 |

---

## 1.2 Team Authorship & Work Ownership Matrix (Team of Two)

```
┌────────────────────────────────────────────────────────┐
│                   HARI DEV SHAJI                       │
│                     (12313476)                         │
│  • Part I: Problem Context, Behavioral Foundations     │
│  • Part II: ReAct Agent Loop & Groq LPU Gateway        │
│  • Dynamic Onboarding ("➕ Add New User" Subsystem)    │
│  • Output Token Sanitization Pipeline (_clean_reply)   │
│  • Project Presentation Slides: 1 to 5                 │
└───────────────────────────┬────────────────────────────┘
                            │
              Shared Architecture & Interfaces
                            │
┌───────────────────────────┴────────────────────────────┐
│                    NIKHIL SINGH                        │
│                     (12323695)                         │
│  • Part II: SQLite Relational Schema & Indices         │
│  • Zero-Mean Gaussian Biometric Synthesizer N(0, σ)   │
│  • Deterministic Clinical Red-Flag Safety Triage       │
│  • Part III: 8-Part Pytest Verification & Case Studies │
│  • Project Presentation Slides: 6 to 10                │
└────────────────────────────────────────────────────────┘
```

### Table 1: Complete Work Division and Deliverables Ownership

| Topic / Component | Primary Owner | Secondary Contributor | Concrete Deliverables & Artifacts |
| :--- | :---: | :---: | :--- |
| **Problem Formulation & Clinical Gap** | **Haridev Shaji (12313476)** | Nikhil Singh (12323695) | Analysis of stateless conversational failure; behavioral science models (TTM, BJ Fogg). |
| **Autonomous ReAct Agent & Tool Loop** | **Haridev Shaji (12313476)** | Nikhil Singh (12323695) | Multi-turn reasoning loop in `agent.py`; 5 tool JSON schemas; system prompt negative constraints. |
| **Groq LPU Gateway & API Resilience** | **Haridev Shaji (12313476)** | Nikhil Singh (12323695) | `qwen/qwen3.8-27b` selection; 4-stage exponential backoff handling HTTP 429 rate limits. |
| **Dynamic User Onboarding Subsystem** | **Haridev Shaji (12313476)** | Nikhil Singh (12323695) | "➕ Add New User" sidebar UI; dynamic UID generation; tailored onboarding prompt generator. |
| **Output Token Sanitization Pipeline** | **Haridev Shaji (12313476)** | Nikhil Singh (12323695) | Multi-regex `_clean_reply` stripping `<tool_call>` XML blocks and robotic developer meta-talk. |
| **Relational Database Design (SQLite)** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | 4-table relational schema (`users`, `sessions`, `memories`, `advice_log`) with foreign key cascades. |
| **Longitudinal Biometric Telemetry** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | 4-week daily synthetic data generator with zero-mean normalized Gaussian noise $\mathcal{N}(0, \sigma^2)$. |
| **Deterministic Clinical Safety Triage** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | Hardcoded pre-LLM regex interceptor in `safety.py` halting execution for acute red flags. |
| **Automated Testing & Benchmark Suite** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | 8/8 automated Pytest test suite in `tests/test_all.py` (passes 100% in 0.77s). |
| **Empirical Persona Case Studies** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | Longitudinal evaluations of Aarav (`p01`), Meera (`p02`), Rohan (`p03`), and custom user Hari. |
| **Deployment & Seeder Infrastructure** | Nikhil Singh (12323695) | **Haridev Shaji (12313476)** | Sub-second database seeder (`seed_demo_data.py`); Streamlit Community Cloud and Render deployment setup. |

---

# SECTION 2: COMPLETE TABLE OF CONTENTS

```text
Table of Contents:
Abstract .................................................................... 3
Team Organization and Work Division ......................................... 4
Part I — Problem Context, Clinical Foundations and Solution Concept ......... 5
    1.1 Project Introduction & Preventable Disease Burden .................. 5
    1.2 The Dilemma of Modern Conversational Agents in Healthcare ........... 6
    1.3 Clinical Foundations of Habit Formation (TTM & BJ Fogg) ............. 7
    1.4 Introducing the CareCompanion Paradigm .............................. 8
    1.5 Problem Statement and Academic Requirements Mapping ................. 9
Part II — System Architecture, Database and Agent Reasoning ................. 10
    2.1 System Architecture and Layered 4-Tier Orchestration ................ 10
    2.2 Dual-Brain Execution Pipeline (Groq LPU vs. Offline State Machine) .. 11
    2.3 Relational Database Schema and 3NF Modeling ......................... 12
    2.4 Synthetic Telemetry Generator with Zero-Mean Weekly Gaussian Drift .. 13
    2.5 Mathematical Derivation: Proof of Zero Baseline Drift ............... 14
    2.6 Autonomous Agentic Tool Pipeline (The 5 Specialized Tools) .......... 15
    2.7 Complete OpenAI-Compatible Tool Function JSON Schemas ............... 16
    2.8 Cross-Session Episodic Reflection and Importance Scoring (I in 1..5). 17
    2.9 Biometric Outcome Tracking and Closed-Loop Strategy Adaptation ...... 18
    2.10 Output Token Sanitization and Anti-Leak Filtering Pipeline ......... 19
    2.11 Deterministic Clinical Red-Flag Safety Guardrails .................. 20
    2.12 Security Threat Modeling, Prompt Injection & Adversarial Robustness . 21
    2.13 Detailed Code Walkthrough of ReAct Orchestration Loop .............. 22
Part III — Implementation, Verification, Empirical Results and Roadmap ...... 23
    3.1 Technology Stack and Architectural Justifications ................... 23
    3.2 User Interface and Interactive Experience (Streamlit Web App) ....... 24
    3.3 Dynamic User Creation Subsystem ('➕ Add New User') ................. 25
    3.4 Longitudinal Biometric Telemetry Statistics ......................... 26
    3.5 Testing Methodology and Automated Pytest Verification Suite ......... 27
    3.6 Empirical Evaluation: Persona p01 (Aarav - Sleep Latency) ........... 28
    3.7 Empirical Evaluation: Persona p02 (Meera - Step Count Pivot) ........ 29
    3.8 Empirical Evaluation: Persona p03 (Rohan - Stress Recovery) ......... 30
    3.9 Empirical Evaluation: Custom Registered User (Hari - Onboarding) .... 31
    3.10 Comparative Analysis with Commercial Digital Health Platforms ...... 32
    3.11 Technical Challenges, Failure Modes and Engineering Solutions ...... 33
    3.12 Current Limitations and Safety Boundaries .......................... 34
    3.13 Future Research and Development Roadmap (Phases 1, 2, 3) ........... 35
    3.14 Conclusion and Summary ............................................. 36
References .................................................................. 37
Appendix A — Quick Start and Terminal Execution Guide ....................... 38
Appendix B — Relational Database SQL Schema DDL ............................. 39
Appendix C — Standardized Benchmark Personas and Dynamic Profiles ........... 40
Appendix D — Glossary of Agentic and Clinical Terminology ................... 41
Appendix E — Complete Python Code Implementations ........................... 42
```

---

# SECTION 3: DETAILED TECHNICAL CONTENT BY PART

## 3.1 PART I: Problem Context, Clinical Foundations & Solution Concept
*(Authored by: Haridev Shaji — Registration No. 12313476)*

### 1.1 Project Introduction & Preventable Disease Burden
Preventable lifestyle-related chronic conditions—principally metabolic syndrome, Type 2 diabetes mellitus, cardiovascular disease, hypertension, and circadian sleep disorders—account for approximately 74% of premature deaths globally according to the World Health Organization. Clinical trials repeatedly demonstrate that sustained lifestyle interventions (regular daily ambulation of 7,000–10,000 steps, structured sleep hygiene, and progressive cardiovascular exercise) produce risk reductions equal or superior to primary pharmacological therapies. 

However, conventional delivery of lifestyle coaching suffers from three crippling economic and structural barriers:
1. **Severe Cost Asymmetry:** Certified wellness coaches charge $80–$250 per hour, rendering regular behavioral guidance inaccessible to the majority of patients.
2. **Caseload Cognitive Fatigue:** Human practitioners managing hundreds of clients struggle to track longitudinal trend lines across wearable device streams, frequently relying on fallible, hand-written clinical notes.
3. **Discontinuous Care:** Consultations occur bi-monthly or quarterly, allowing behavioral relapses to persist unnoticed for weeks.

### 1.2 The Dilemma of Modern Conversational Agents in Healthcare
Deploying out-of-the-box LLMs (ChatGPT, Claude, or mobile health assistants) into healthcare coaching fails because of three architectural pathologies:
- **Ephemeral Context Erasure:** When a chat session terminates or context window limits are reached, all historical context is wiped. When a client returns one week later and remarks: *"My knee feels worse after following your advice,"* a stateless LLM has no knowledge of what exercise was prescribed, why it was chosen, or what underlying joint pathology was previously disclosed.
- **Open-Loop Hallucination:** LLMs generate statistically likely text without verifying ground truth. If a coach suggests that a sedentary user begin jogging 5 km daily, and wearable sensor streams show that daily steps actually plummeted due to exhaustion, a stateless LLM cannot correlate the biometric failure with its prior recommendation. It blindly repeats variations of the failed plan.
- **Diagnostic Sycophancy & Liability:** When faced with acute medical emergencies (e.g., chest tightness, shortness of breath), unconstrained LLMs frequently attempt conversational comfort or home remedies, catastrophically delaying life-saving clinical care.

### 1.3 Clinical Foundations of Habit Formation (TTM & BJ Fogg)
CareCompanion grounds its algorithmic reasoning in two established behavioral psychology frameworks:
- **Transtheoretical Model of Behavior Change (TTM):** Prochaska and DiClemente establish that habit progression moves across discrete stages: *Precontemplation $\rightarrow$ Contemplation $\rightarrow$ Preparation $\rightarrow$ Action $\rightarrow$ Maintenance*. Stateless agents consistently fail by demanding aggressive Action-stage behaviors from Contemplation-stage users. CareCompanion uses conversational intake to tailor intervention difficulty.
- **BJ Fogg Behavior Model ($B = M \times A \times P$):** Dr. B.J. Fogg demonstrates that behavior occurs only when Motivation ($M$), Ability ($A$), and a Prompt ($P$) converge. When motivation dips, an intervention fails unless Ability is drastically increased by lowering friction (e.g., micro-habits). CareCompanion implements automated strategy pivots that systematically lower physical friction when an initial plan stalls.

### 1.4 Introducing the CareCompanion Paradigm
CareCompanion solves these challenges through an autonomous closed-loop architecture:
- Natural-language interface requiring zero SQL or programming expertise.
- Deterministic pre-LLM safety gating that intercepts acute medical red-flags before LLM execution.
- Autonomous ReAct tool execution loop where every numerical assertion is derived strictly from database records.
- Transactional SQLite memory persisting profile data, session summaries, and physical contraindications.
- Quantitative closed-loop outcome verification that compares sensor telemetry against historical advice baselines.
- Multi-tier output sanitization pipeline ensuring conversational warmth and eliminating tool token leaks.
- Dual-brain execution architecture guaranteeing 100% operational reliability offline or during cloud outages.

---

## 3.2 PART II: System Architecture, Database & Agent Reasoning
*(Authored jointly by: Haridev Shaji & Nikhil Singh)*

### 2.1 4-Tier Layered Architecture
- **Tier 1 (Presentation):** Streamlit Web UI (`app.py`) with persona selector, 28-day telemetry charts, persistent memory inspector, and chat interface; headless evaluation CLI (`demo.py`).
- **Tier 2 (Reasoning):** `CareAgent` class (`agent.py`) managing session lifecycles, ReAct loop orchestration, brain selection (Groq LPU vs. offline planner), and output sanitization (`_clean_reply`).
- **Tier 3 (Execution & Tools):** `ToolBox` class (`tools.py`) exposing 5 validated tools, deterministic safety interceptor (`safety.py`), and episodic reflection engine (`reflection.py`).
- **Tier 4 (Persistence):** SQLite database (`data/carecompanion.db`) storing relational tables, alongside synthetic biometric datastore (`data/synthetic/<uid>/daily.csv`).

### 2.2 Dual-Brain Execution Pipeline
- **Cloud Brain (Groq LPU Gateway):** Invokes Groq LPUs running `qwen/qwen3.8-27b` via OpenAI-compatible function calling. Incorporates 4-stage exponential backoff in `llm.py` ($\text{Delay} = 8 \times (\text{attempt} + 1)$ seconds) to handle HTTP 429 rate limits.
- **Offline Brain (Deterministic Planner):** If no API key is set, or upon repeated cloud errors, the agent falls back to `mock_llm.py`. Using regular-expression slot parsing, it routes intents to the identical 5 tools and compiles natural, supportive responses from clinical templates.

### 2.3 Relational Database Schema & Data Modeling
The SQLite database (`data/carecompanion.db`) enforces referential integrity across 4 tables:
```sql
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_num INTEGER NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS memories (
    memory_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    importance INTEGER NOT NULL CHECK(importance BETWEEN 1 AND 5),
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS advice_log (
    advice_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_num INTEGER NOT NULL,
    topic TEXT NOT NULL,
    strategy TEXT NOT NULL,
    baseline_val REAL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id);
CREATE INDEX IF NOT EXISTS idx_advice_user ON advice_log(user_id, topic);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
```

### 2.4 Synthetic Telemetry Generator with Zero-Mean Weekly Gaussian Drift
Synthesizes 28 days (4 weeks) of wearable sensor data (`carecompanion/synthetic.py`).
To prevent random-walk baseline drift while preserving biological daily variance:
For metric $m$ across week $w$:
1. Sample 7 raw perturbations: $\xi_i \sim \mathcal{N}(0, \sigma_m^2)$ for $i \in \{0, \dots, 6\}$.
2. Calculate sample mean: $\mu = \frac{1}{7} \sum_{i=0}^{6} \xi_i$.
3. Compute zero-mean normalized noise: $\delta_i = \xi_i - \mu \implies \sum_{i=0}^{6} \delta_i = 0$.
4. Calculate synthesized daily value: $X_m(7w + i) = \text{round}\left( \bar{X}_m[w] + \delta_i \right)$.

**Mathematical Proof of Zero Baseline Drift:**
$$\frac{1}{7} \sum_{i=0}^{6} X_m(7w + i) = \frac{1}{7} \sum_{i=0}^{6} \left( \bar{X}_m[w] + \delta_i \right) = \bar{X}_m[w] + \frac{1}{7} \sum_{i=0}^{6} \delta_i = \bar{X}_m[w] + 0 = \bar{X}_m[w] \quad \text{(Q.E.D.)}$$

Variance scaling factors:
- $\sigma_{\text{steps}} = 0.08 \times \bar{X}_{\text{steps}}$ (8% daily coefficient of variation)
- $\sigma_{\text{sleep}} = 0.35\text{ hours}$ (21 minutes daily variance)
- $\sigma_{\text{RHR}} = 1.0\text{ bpm}$
- $\sigma_{\text{calories}} = 80\text{ kcal}$

### 2.5 The 5 Specialized Agent Tools
All tools return a `ToolResult(ok, summary, data)` dataclass:
1. `get_user_profile(user_id)`: Retrieves demographic profile, name, and total session count.
2. `recall_memories(user_id, query)`: Retrieves memories filtered by semantic keywords, sorted by importance ($I \in [1,5]$).
3. `get_health_summary(user_id, days)`: Computes rolling average, min, and max across 7, 14, or 28 days of sensor telemetry.
4. `check_advice_outcomes(user_id)`: Compares past advice baselines against current 7-day wearable averages to calculate delta % and status (`improved`, `no_change`, `worse`).
5. `log_advice(user_id, topic, strategy)`: Records agreed strategy and baseline sensor value to `advice_log`.

### 2.6 Closed-Loop Outcome Tracking & Strategy Modification
When a returning user starts a consultation, `check_advice_outcomes` calculates the relative percentage delta ($\Delta$):
$$\Delta = \frac{\bar{X}_{\text{current}} - X_{\text{baseline}}}{X_{\text{baseline}}} \times 100\%$$
- **$\Delta \ge +5.0\% \implies \text{"improved"}$:** Strategy succeeds; coach validates agency, celebrates win, and increments load.
- **$-5.0\% < \Delta < +5.0\% \implies \text{"no\_change"}$:** Strategy has stalled; coach acknowledges barrier without blame and **must pivot to a new strategy**.
- **$\Delta \le -5.0\% \implies \text{"worse"}$:** Regression; coach lowers friction or eliminates the prompt entirely.

### 2.7 Episodic Reflection & Importance Weighting ($I \in [1,5]$)
At session termination (`agent.end_session()`), the dialogue transcript is distilled into atomic facts:
- **$I = 5$ (Critical Safety Constraint):** Physical injuries, joint pain, surgical history, clinical contraindications.
- **$I = 4$ (Primary Health Goal):** Explicit target objectives (train for 10K, resolve insomnia).
- **$I = 3$ (Lifestyle Constraint):** Shift work, long commute, travel schedule.
- **$I = 2$ (Personal Preference):** Modality preferences (outdoor walks vs. gym).
- **$I = 1$ (Incidental Context):** Minor conversational remarks.

### 2.8 Anti-Leak Output Token Sanitizer (`_clean_reply`)
To prevent open-source models on Groq from leaking internal tool syntax into user chat bubbles, `_clean_reply()` executes a multi-stage regex pipeline:
```python
def _clean_reply(text: str) -> str:
    # 1. Strip raw XML tool_call blocks
    text = re.sub(r"<tool_call>[\s\S]*?</tool_call>", "", text, flags=re.IGNORECASE)
    # 2. Strip stray parameter tags
    text = re.sub(r"</?(?:function|parameter|tool_call)[^>]*>", "", text, flags=re.IGNORECASE)
    # 3. Suppress developer meta-text
    text = re.sub(
        r"(?:I need to|Let me|I have saved|I will save).*?(?:memory|database|profile|records?)\.?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\n{3,}", "\n\n", text).strip()
```

### 2.9 Deterministic Pre-LLM Clinical Safety Guardrails
Before invoking LLM reasoning, `carecompanion/safety.py` screens every user prompt against critical red-flag symptoms:
- *Myocardial Infarction / Angina:* Substernal chest pressure, radiating arm/jaw pain.
- *Cerebrovascular Accident (Stroke):* Facial drooping, unilateral arm weakness, slurred speech.
- *Acute Dyspnea:* Severe shortness of breath, respiratory distress.
- *Syncope / Neurotrauma:* Loss of consciousness, sudden severe headache.

If matched, execution halts immediately and returns a hardcoded clinical emergency notice:
> *"⚠️ MEDICAL EMERGENCY DETECTED: Your symptoms require immediate emergency care. Please call 911/112 or visit the nearest emergency room immediately."*

---

## 3.3 PART III: Implementation, Verification, Empirical Results & Future Scope
*(Authored by: Nikhil Singh — Registration No. 12323695)*

### 3.1 Technology Stack & Architectural Decisions
- **Language:** Python 3.10–3.12 (Native type hints, robust ecosystem).
- **Web Dashboard:** Streamlit 1.36+ (Zero JavaScript build overhead, native reactive components).
- **Relational Storage:** SQLite (Built-in, zero configuration, ACID-compliant, single-file portability).
- **LLM Gateway:** OpenAI Python SDK 1.40+ (Used with Groq LPU endpoint for `qwen/qwen3.8-27b`).
- **Secrets Management:** `python-dotenv` 1.0+ (Strict separation of environment variables from source).
- **Test Harness:** Pytest 8.0+ (Sub-second headless test discovery).

### 3.2 Dynamic User Creation ("➕ Add New User")
Evaluators can create custom profiles live from the Streamlit sidebar:
1. Enter custom Name (e.g., `Hari`) and select Goal (`Steps`, `Sleep`, `Cardio`).
2. System allocates unique ID `u_hari`, provisions a 4-week synthetic baseline stream (`daily.csv`), and registers the user in SQLite.
3. Automatically compiles dynamic onboarding starter prompts in `carecompanion/scripts.py`.

### 3.3 Automated Pytest Verification Suite
The test harness (`tests/test_all.py`) runs 8 automated unit/integration tests completely offline in **0.77 seconds**:

| Test Name | Module | Scope | Result |
| :--- | :--- | :--- | :---: |
| `test_database_init_and_user_creation` | `db.py` | Schema creation, user insertion, session increments | **PASS** |
| `test_memory_storage_and_retrieval` | `memory.py` | Memory upserts, keyword ranking by importance | **PASS** |
| `test_advice_logging_and_outcome_tracking` | `tools.py` | Baseline recording, $\pm 5\%$ deadband classification | **PASS** |
| `test_synthetic_data_generation` | `synthetic.py` | 28-day data completeness, zero-mean weekly noise | **PASS** |
| `test_agent_reasoning_and_tool_call` | `agent.py` | Multi-turn ReAct tool execution loop | **PASS** |
| `test_safety_guardrails_red_flag` | `safety.py` | Deterministic interception of chest pain | **PASS** |
| `test_agent_survives_llm_failure` | `llm.py` | Seamless fallback to offline planner on API error | **PASS** |
| `test_reflection_extracts_durable_facts`| `reflection.py`| Dialogue distillation, assigning $I=5$ for injuries | **PASS** |

### 3.4 Multi-Session Empirical Case Studies

#### 1. Persona `p01` (Aarav - Sleep Focus)
- **Baseline (Week 1):** Average sleep: 5.8 hours/night (severe sleep debt).
- **Session 1:** Coach logs advice: *11 PM bedtime routine with screens turned off 30 minutes prior*.
- **Session 2 (Week 2):** Wearable data reflects 6.7 hours/night ($+15.5\%$, `improved`). Coach validates agency and reinforces routine.
- **Session 3 (Week 4):** Sleep reaches 7.2 hours/night ($+24.1\%$). Coach transitions into long-term maintenance.

#### 2. Persona `p02` (Meera - Steps Focus & Strategy Pivot)
- **Baseline (Week 1):** 3,500 steps/day (highly sedentary). Discloses mild knee pain when running ($I=5$).
- **Session 1:** Coach logs Strategy A: *Park 10 minutes away from office entrance to get morning steps*.
- **Session 2 (Week 2):** Wearable data reflects 3,600 steps/day ($+2.8\%$, `no_change`). Morning schedule caused parking friction. Coach acknowledges the stall and **pivots to Strategy B**: *Two 10-minute brisk walks scheduled directly after lunch and dinner*.
- **Session 3 (Week 4):** Steps surge to 5,400 (Week 3) and 5,600 (Week 4), yielding $+55.5\%$ (`improved`). When Meera asks: *"Should I start running 5 miles on the treadmill tomorrow?"*, the agent retrieves the knee pain memory from Session 1 and warns against high-impact treadmill running, advising low-impact walking or elliptical instead.

#### 3. Persona `p03` (Rohan - Exam Stress & Sleep)
- **Baseline (Week 1):** High physical activity (9,500 steps/day), but sleep is 5.5 hours/night with elevated resting heart rate (70 bpm) due to exams.
- **Session 1:** Coach logs Strategy A: *Aggressive 10 PM bedtime alarm*.
- **Session 2 (Week 2):** Sleep remains at 5.6 hours/night ($+1.8\%$, `no_change`). Bedtime alarm created stress. Coach pivots to Strategy B: *10 minutes of evening box breathing and light dimming at 10 PM*.
- **Session 3 (Week 4):** Sleep recovers to 7.1 hours/night, while RHR drops from 70 to 67 bpm (`improved`).

#### 4. Custom Registered User (`u_hari` - Cardiovascular Conditioning)
- **Session 1 (Intake):** Evaluator creates profile 'Hari' with focus on lowering resting heart rate. User discloses: *"I had shoulder surgery 6 months ago, so no push-ups or heavy overhead lifting."* System logs injury constraint ($I=5$). Coach prescribes low-impact incline treadmill walks.
- **Session 2 (Safety Check):** User asks: *"Can I do heavy dumbbell shoulder presses today?"* Agent calls `recall_memories`, retrieves shoulder surgery record, and blocks the contraindicated exercise, proposing leg press and recumbent cycling instead.

---

# SECTION 4: COMPLETE CONSULTATION TRANSCRIPTS (EMPIRICAL BENCHMARKS)

### Dialogue Transcript: Meera (`p02`) — Multi-Session Closed-Loop Adaptation

```text
================================================================================
SESSION 1: INTAKE & BASELINE PRESCRIPTION
================================================================================
[User]: Hi coach, I want to start moving more. I sit at my desk all day and feel sluggish.
[Tool Call]: get_user_profile(user_id="p02")
[Tool Result]: {"name": "Meera", "session_count": 0, "goal": "Increase Daily Steps"}
[Tool Call]: get_health_summary(user_id="p02", days=7)
[Tool Result]: {"avg_steps": 3500, "avg_sleep": 7.2, "avg_rhr": 74}
[Assistant]: Hello Meera! Welcome to CareCompanion. Looking at your recent sensor 
data, you're currently averaging about 3,500 steps a day, while your sleep is solid 
at 7.2 hours. Before we design a plan, do you have any physical injuries or joint 
issues I should know about?

[User]: Yes, I have mild knee pain if I run or do high-impact jumps, so running is out.
[Tool Call]: log_advice(user_id="p02", topic="steps", strategy="Park 10 minutes away from office entrance")
[Tool Result]: {"status": "logged", "baseline_val": 3500}
[Assistant]: Thank you for telling me, Meera. We will strictly avoid running or high-impact 
jumping to protect your knees. To build your step count gently without irritating your 
joints, let's start with a low-friction habit: try parking about 10 minutes away from your 
office entrance. That will give you an easy 1,000 steps each morning without extra gym time!

[Session Ended -> Reflection Routine Extracted]:
- Memory Category: "injury", Content: "Mild knee pain; contraindicates running & high-impact exercises", Importance: 5
- Memory Category: "goal", Content: "Increase daily physical activity and step count", Importance: 4

================================================================================
SESSION 2: ONE-WEEK FOLLOW-UP (STRATEGY FAILURE & ADAPTIVE PIVOT)
================================================================================
[User]: Hey coach, checking in after a week.
[Tool Call]: check_advice_outcomes(user_id="p02")
[Tool Result]: {
    "topic": "steps", 
    "strategy": "Park 10 minutes away from office entrance", 
    "baseline": 3500, 
    "current_7d_avg": 3600, 
    "delta_pct": 2.86, 
    "status": "no_change"
}
[Assistant]: Welcome back, Meera! I just checked your sensor logs from this past week. 
Your steps averaged 3,600 per day compared to our 3,500 baseline—an increase of under 3%, 
which shows the parking strategy didn't quite take hold. How did the morning parking 
routine feel for you?

[User]: Honestly, it was too stressful. I was running late for morning meetings twice, 
so I had to park right by the door, and the other days it was raining.
[Tool Call]: log_advice(user_id="p02", topic="steps", strategy="Two 10-minute post-meal walks after lunch and dinner")
[Tool Result]: {"status": "logged", "baseline_val": 3600}
[Assistant]: That makes total sense! If a strategy clashes with your morning schedule, 
forcing it only adds stress. Let's pivot completely: rather than fighting morning traffic, 
how about taking two short 10-minute walking breaks right after lunch and dinner? 
They are easy on your knees, won't interfere with your morning commute, and naturally 
add 1,800 to 2,000 steps every day!

================================================================================
SESSION 3: TWO-WEEK FOLLOW-UP (VERIFICATION & CONSTRAINT ENFORCEMENT)
================================================================================
[User]: Coach, the post-meal walks worked so well! I feel great. Should I start running 
5 miles on the treadmill tomorrow?
[Tool Call]: check_advice_outcomes(user_id="p02")
[Tool Result]: {
    "topic": "steps", 
    "strategy": "Two 10-minute post-meal walks after lunch and dinner", 
    "baseline": 3600, 
    "current_7d_avg": 5600, 
    "delta_pct": 55.56, 
    "status": "improved"
}
[Tool Call]: recall_memories(user_id="p02", query="knee running treadmill")
[Tool Result]: [{"category": "injury", "content": "Mild knee pain; contraindicates running & high-impact exercises", "importance": 5}]
[Assistant]: That is tremendous progress, Meera! Your steps surged to an average of 
5,600 per day—over a 55% jump from where we started. The post-meal routine clearly fits 
your rhythm. 

Regarding running on the treadmill: remembering your knee pain, I strongly advise 
against jumping into a 5-mile run. High-impact treadmill pounding could easily trigger 
a flare-up and derail your fantastic momentum. Let's keep your progress joint-safe: 
stick with your post-meal brisk walks, or try an elliptical machine if you want a 
cardio challenge without the impact!
================================================================================
```

---

# SECTION 5: COMPLETE SPECIFICATIONS FOR ALL 16 FIGURES

Claude must include and reference **all 16 technical figures** below in the compiled report.

| Figure # | Official Figure Title | Type / Format | Exact Technical Content & Data Points |
| :---: | :--- | :--- | :--- |
| **Figure 1** | *Division of Project Responsibilities across Presentation Hand-Overs* | Chevron Flowchart (SVG / Mermaid) | Shows Hand-over from Haridev Shaji (Part I: Slides 1–4, Part II (Agent Core & LLM)) to Nikhil Singh (Part II (Data Architecture & Safety), Part III: Slides 8–10). |
| **Figure 2** | *Traditional Stateless Conversational AI Workflow vs. CareCompanion Closed-Loop Paradigm* | Comparative Diagram (SVG / ASCII) | Left: Prompt $\rightarrow$ Context Purge $\rightarrow$ Hallucinatory Advice $\rightarrow$ Injury Risk. Right: Prompt $\rightarrow$ Pre-LLM Safety $\rightarrow$ Relational Memory $\rightarrow$ Biometric Telemetry $\rightarrow$ Closed-Loop Audit $\rightarrow$ Sanitizer $\rightarrow$ Grounded Coaching. |
| **Figure 3** | *Longitudinal 4-Week Habit Progression and Outcome Evaluation Cycle* | Biometric Line Chart (Matplotlib / SVG) | Week 1: Baseline (3,500) $\rightarrow$ Week 2: Initial Advice (3,600, Stalled) $\rightarrow$ Strategy Pivot $\rightarrow$ Week 3: (5,400) $\rightarrow$ Week 4: Target (5,600). |
| **Figure 4** | *Layered 4-Tier System Architecture of CareCompanion* | Architecture Block Diagram (SVG / Mermaid) | Tiers 1–4: Presentation (`app.py`, `demo.py`), Reasoning (`agent.py`, `llm.py`, `mock_llm.py`), Execution (`tools.py`, `safety.py`), Persistence (`carecompanion.db`, `daily.csv`). |
| **Figure 5** | *Synthetic Biometric Telemetry Generation Pipeline with Zero Baseline Drift* | Mathematical Pipeline Flowchart | Target Weekly Means $\rightarrow$ Gaussian Noise $\mathcal{N}(0,\sigma^2)$ $\rightarrow$ Mean Subtraction ($\mu = \frac{1}{7}\sum \xi_i$) $\rightarrow$ Zero-Mean Daily Perturbation ($\sum \delta_i = 0$) $\rightarrow$ CSV Storage. |
| **Figure 6** | *Relational Database Entity-Relationship Diagram (SQLite 3NF Schema)* | ER Diagram (Mermaid / SVG) | 4 Tables: `users` (1 to N) `sessions`, `users` (1 to N) `memories`, `users` (1 to N) `advice_log`. Shows PKs, FKs, and cascade delete rules. |
| **Figure 7** | *Autonomous Agentic Tool Execution and Parameter Validation Path* | Sequence Flow Diagram | User Prompt $\rightarrow$ `CareAgent` $\rightarrow$ JSON Schema Validation $\rightarrow$ `ToolBox.call()` $\rightarrow$ SQLite Query $\rightarrow$ Standardized `ToolResult`. |
| **Figure 8** | *Dual-Brain Orchestration Pipeline with Automated 4-Stage Fallback* | Decision Tree / Flowchart | Prompt $\rightarrow$ Cloud Key Check $\rightarrow$ Groq LPU (`qwen/qwen3.8-27b`) $\rightarrow$ HTTP 429? $\rightarrow$ Exponential Backoff ($8 \times (\text{att}+1)$) $\rightarrow$ Fail? $\rightarrow$ Local Offline Planner (`mock_llm.py`). |
| **Figure 9** | *ReAct Autonomous Execution Loop and Clinical Safety Safeguards* | ReAct State Machine | State 1: Reason (Parse prompt + history) $\rightarrow$ State 2: Act (Invoke tool) $\rightarrow$ State 3: Observe (Parse `ToolResult`) $\rightarrow$ State 4: Respond (Sanitize reply). Bounded to $\le 6$ steps. |
| **Figure 10** | *UML Sequence Diagram for Closed-Loop Outcome Verification* | UML Sequence Diagram | User $\rightarrow$ UI $\rightarrow$ Agent $\rightarrow$ `check_advice_outcomes` $\rightarrow$ DB $\rightarrow$ Delta % Evaluation $\rightarrow$ Strategy Pivot Response. |
| **Figure 11** | *Source Code Volume Distribution by Subsystem (Lines of Python)* | Horizontal Bar Chart (Matplotlib / SVG) | `agent.py`: 320 lines, `tools.py`: 245 lines, `db.py`: 195 lines, `synthetic.py`: 210 lines, `mock_llm.py`: 260 lines, `app.py`: 280 lines, `test_all.py`: 215 lines, `scripts.py`: 110 lines. Total: ~1,835 lines. |
| **Figure 12** | *Biometric Telemetry Volume Across Benchmark Personas* | Grouped Bar Chart (Matplotlib / SVG) | 28 days of data per user. Aarav (`p01`), Meera (`p02`), Rohan (`p03`), Hari (`u_hari`). Total: 112 daily records, 448 physiological data points. |
| **Figure 13** | *Longitudinal Step Count Trajectory for Persona p02 (Meera)* | Step Chart / Line Graph (Matplotlib / SVG) | Day 1–7: ~3,500 steps/day. Day 8–14: ~3,600 steps/day. Day 15–21: ~5,400 steps/day. Day 22–28: ~5,600 steps/day. Annotates strategy pivot on Day 14. |
| **Figure 14** | *Automated Pytest Suite Results by Architectural Subsystem* | Status / KPI Chart | 8 tests passing: Database (0.05s), Memory (0.04s), Advice Logging (0.06s), Telemetry (0.12s), Agent Loop (0.08s), Safety (0.03s), Fallback (0.07s), Reflection (0.06s). Total: 0.77s. |
| **Figure 15** | *Headline Empirical Results Across Benchmark Personas* | Paired Column Bar Chart (Matplotlib / SVG) | Aarav Sleep: 5.8h $\rightarrow$ 7.2h (+24.1%). Meera Steps: 3,500 $\rightarrow$ 5,600 (+55.5%). Rohan RHR: 70 bpm $\rightarrow$ 67 bpm (-4.3%). |
| **Figure 16** | *Three-Phase Research and Development Roadmap (2027–2028)* | Multi-Phase Chevron Roadmap | Phase 1 (Q1–Q2 2027: Apple HealthKit/BLE), Phase 2 (Q3–Q4 2027: Vector Embeddings & Vision Food Diary), Phase 3 (2028: IRB Clinical Trial). |

---

# SECTION 6: PYTHON MATPLOTLIB CODE FOR GENERATING REPORT CHARTS

Claude can reference or output this Python script to produce the exact figures:

```python
"""
Plotting script for CareCompanion Academic Project Report Figures.
Generates Figures 11, 13, 14, and 15 matching the report data.
"""
import matplotlib.pyplot as plt
import numpy as np

# Palette matching FloatChat / CareCompanion theme
NAVY = "#0F4C81"
TEAL = "#0D9488"
ORANGE = "#E06D3B"
GRAY = "#64748B"

# Figure 11: Lines of Python per Module
def plot_figure_11():
    modules = ['scripts.py', 'test_all.py', 'db.py', 'synthetic.py', 'tools.py', 'mock_llm.py', 'app.py', 'agent.py']
    lines = [110, 215, 195, 210, 245, 260, 280, 320]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(modules, lines, color=TEAL, edgecolor=NAVY)
    ax.set_xlabel('Lines of Python Code', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title('Figure 11: Source Code Volume Distribution by Subsystem (~1,835 Lines)', fontsize=12, fontweight='bold', color=NAVY)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 5, bar.get_y() + bar.get_height()/2, f'{int(w)}', va='center', fontsize=9, color=NAVY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('figure_11_code_distribution.png', dpi=300)

# Figure 13: Meera Step Trajectory
def plot_figure_13():
    days = np.arange(1, 29)
    # 4 weeks of synthesized data
    w1 = np.random.normal(3500, 150, 7)
    w2 = np.random.normal(3600, 180, 7)
    w3 = np.random.normal(5400, 200, 7)
    w4 = np.random.normal(5600, 190, 7)
    steps = np.concatenate([w1, w2, w3, w4])
    
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(days, steps, marker='o', markersize=4, color=TEAL, linewidth=2, label='Daily Steps')
    ax.axhline(3500, color=GRAY, linestyle='--', label='Week 1 Baseline (3,500)')
    ax.axvline(14, color=ORANGE, linestyle=':', linewidth=2, label='Strategy Pivot (Day 14)')
    ax.axhline(5600, color=NAVY, linestyle='--', label='Week 4 Target (5,600)')
    
    ax.set_xlabel('Day of Program (4 Weeks)', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel('Daily Step Count', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title('Figure 13: Persona p02 (Meera) Longitudinal Step Count Trajectory', fontsize=12, fontweight='bold', color=NAVY)
    ax.legend(loc='lower right', frameon=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('figure_13_meera_trajectory.png', dpi=300)

# Figure 15: Headline Results
def plot_figure_15():
    metrics = ['Aarav (Sleep hrs)', 'Meera (Steps/100)', 'Rohan (RHR bpm)']
    baseline = [5.8, 35.0, 70.0]
    final = [7.2, 56.0, 67.0]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    r1 = ax.bar(x - width/2, baseline, width, label='Baseline (Week 1)', color=ORANGE)
    r2 = ax.bar(x + width/2, final, width, label='Final Outcome (Week 4)', color=TEAL)
    
    ax.set_ylabel('Metric Value', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title('Figure 15: Headline Empirical Biometric Adaptations Across Personas', fontsize=12, fontweight='bold', color=NAVY)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold')
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('figure_15_headline_results.png', dpi=300)

if __name__ == '__main__':
    plot_figure_11()
    plot_figure_13()
    plot_figure_15()
    print("All report figures plotted successfully.")
```

---

# SECTION 7: ANTI-AI DETECTOR GUIDELINES & ACADEMIC HUMANIZATION RULES

To guarantee that the report compiles as **100% human-written** and completely bypasses AI detectors (GPTZero, Turnitin, Copyleaks), Claude must adhere to the following stylistic directives:

1. **Sentence Burstiness & Varied Cadence:**  
   Mix ultra-short declarative sentences with compound analytical arguments. Avoid uniformly structured 20-word compound sentences.  
   *Example:* *"API failures happen. Rather than crashing the web interface, CareCompanion catches the exception in `llm.py` and silently routes the user's intent through `mock_llm.py`."*
2. **First-Person Team Narrative:**  
   Use natural team phrasing where appropriate: *"During initial trials on Groq, we noticed the Qwen model emitting raw `<tool_call>` tags into user chat windows. We resolved this by building a dedicated regex cleaner..."*
3. **Realistic Technical Frustrations & Edge Cases:**  
   Describe real engineering trade-offs: why SQLite was selected over PostgreSQL for local evaluation, why Groq's `qwen/qwen3.8-27b` replaced the deprecated `llama-3.3-70b-versatile` endpoint, and why rectangular deadbands ($\pm 5\%$) were chosen over continuous rolling curves.
4. **Concrete Numerical Anchoring:**  
   Ground every claim in physical units: `dbar`, `bpm`, `steps/day`, `hours/night`, `milliseconds`, `0.77s execution time`, `8 out of 8 tests`.
5. **No AI Structural Formula:**  
   Do not start every paragraph with transitional conjunctions (*"Moreover"*, *"Furthermore"*, *"Additionally"*, *"In light of this"*). Begin directly with the technical subject or action verb.

---

*(This document represents the complete, definitive technical knowledge base for CareCompanion. Claude can now generate the full 20 to 25 page academic project report matching all requirements.)*
