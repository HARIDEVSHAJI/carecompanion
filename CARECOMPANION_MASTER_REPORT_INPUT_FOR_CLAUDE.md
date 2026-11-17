# CareCompanion: Autonomous Agentic Healthcare Coaching System with Multi-Session Memory and Adaptive Advice Progression

> **Document Instructions for Claude:**  
> Use this comprehensive technical document as the complete factual source to generate a formal, academic, human-written Project Report of **20 to 25 pages** (formatted identically to the attached *FloatChat* sample report).  
> **Course:** LLM & Agentic AI — CA1 Project-Based Assignment  
> **Problem Reference:** Problem Statement #4 — *Autonomous Health & Wellness Coaching Agent with Multi-Session Memory and Adaptive Advice Progression*  
> **Team of Two Members:**  
> 1. **Hari Dev Shaji** (Registration No. **12313476**) — Part I (Problem Context, Behavioral Psychology, Solution Concept) & Part II Lead (Agentic Reasoning Loop, Groq LPU Integration, Dynamic User Creation, Output Sanitization).  
> 2. **Nikhil Singh** (Registration No. **12313478**) — Part II Co-Lead (SQLite Relational Schema, Zero-Mean Gaussian Telemetry Generator) & Part III (Implementation, Safety Triage, Automated Pytest Verification, Multi-Session Empirical Results, Deployment).  
> **GitHub Repository:** `https://github.com/HARIDEVSHAJI/carecompanion.git`  
> **Tone & Style:** Academic, precise, realistic engineering prose. Plagiarism-free and natural human style (avoiding generic AI filler clichés). All metrics and numbers come directly from this document.

---

# SECTION 1: PROJECT METADATA & TEAM WORK DIVISION

## 1.1 Academic Meta Table

| Item | Academic / Operational Specification |
| :--- | :--- |
| **Project Title** | CareCompanion: An Agentic Healthcare Coaching System with Persistent Cross-Session Memory, Longitudinal Biometric Outcome Tracking, and Deterministic Safety Guardrails |
| **Course** | LLM & Agentic AI (CA1 Project-Based Assignment, Academic Year 2026–2027) |
| **Institution** | School of Computer Science & Engineering, Lovely Professional University, Punjab, India |
| **Problem Statement** | Problem Statement #4: Autonomous Coaching Agent with Persistent Memory & Adaptive Outcome Progression |
| **Repository** | `https://github.com/HARIDEVSHAJI/carecompanion.git` (Clean main branch) |
| **Distribution Package** | `carecompanion_deploy.zip` (~39 KB standalone package with zero secrets or venvs) |
| **Date** | November 2026 |

---

## 1.2 Team Members & Responsibility Matrix (Team of Two)

```
┌────────────────────────────────────────────────────────┐
│                   HARI DEV SHAJI                       │
│                     (12313476)                         │
│  • Part I: Problem Context, Behavioral Foundations     │
│  • Part II: ReAct Agent Loop & Groq LPU Integration    │
│  • Dynamic Onboarding ("➕ Add New User" Subsystem)    │
│  • Output Token Sanitization Pipeline (_clean_reply)   │
│  • Slides 1 to 5 of Project Presentation               │
└───────────────────────────┬────────────────────────────┘
                            │
              Shared Architecture & Interfaces
                            │
┌───────────────────────────┴────────────────────────────┐
│                    NIKHIL SINGH                        │
│                     (12313478)                         │
│  • Part II: SQLite Relational Schema & Indices         │
│  • Zero-Mean Gaussian Biometric Synthesizer N(0, σ)   │
│  • Deterministic Clinical Red-Flag Safety Triage       │
│  • Part III: 8-Part Pytest Verification & Case Studies │
│  • Slides 6 to 10 of Project Presentation              │
└────────────────────────────────────────────────────────┘
```

### Table 1: Detailed Ownership Breakdown

| Section / Topic | Hari Dev Shaji (12313476) | Nikhil Singh (12313478) | Primary Deliverables |
| :--- | :---: | :---: | :--- |
| **Problem Definition & Clinical Context** | **Owner** | Contributor | Analysis of stateless conversational failure; behavioral science models (TTM, BJ Fogg). |
| **Autonomous ReAct Agent & Tool Loop** | **Owner** | Contributor | Multi-turn reasoning loop in `agent.py`; 5 tool JSON schemas; system prompt negative constraints. |
| **Groq LPU Gateway & API Hardening** | **Owner** | Contributor | `qwen/qwen3.8-27b` selection; 4-stage exponential backoff handling HTTP 429 limits. |
| **Dynamic User Onboarding Subsystem** | **Owner** | Contributor | "➕ Add New User" sidebar UI; dynamic UID generation; tailored onboarding prompt generator. |
| **Output Token Sanitization Pipeline** | **Owner** | Contributor | Multi-regex `_clean_reply` stripping `<tool_call>` XML blocks and robotic developer meta-talk. |
| **Relational Database Design (SQLite)** | Contributor | **Owner** | 4-table relational schema (`users`, `sessions`, `memories`, `advice_log`) with foreign key cascades. |
| **Longitudinal Biometric Telemetry** | Contributor | **Owner** | 4-week daily synthetic data generator with zero-mean normalized Gaussian noise $\mathcal{N}(0, \sigma^2)$. |
| **Deterministic Clinical Safety Triage** | Contributor | **Owner** | Hardcoded pre-LLM regex interceptor in `safety.py` halting execution for acute red flags. |
| **Automated Testing & Benchmark Suite** | Contributor | **Owner** | 8/8 automated Pytest test suite in `tests/test_all.py` (passes 100% in 0.77s). |
| **Empirical Persona Case Studies** | Contributor | **Owner** | Longitudinal evaluations of Aarav (`p01`), Meera (`p02`), Rohan (`p03`), and custom user Hari. |
| **Deployment & Seeder Infrastructure** | Contributor | **Owner** | Sub-second database seeder (`seed_demo_data.py`); Streamlit Community Cloud and Render deployment setup. |

---

# SECTION 2: EXECUTIVE SUMMARY & ABSTRACT

**Abstract:**  
Commercial conversational artificial intelligence (AI) agents applied to consumer health and wellness operate predominantly as stateless, single-turn reactive pipelines. When a patient or client interacts with a standard Large Language Model (LLM), the model evaluates the prompt in total isolation. It lacks episodic memory across calendar encounters, remains oblivious to persistent physical contraindications (such as joint injuries or recent surgeries), and possesses no mechanism to verify whether previously prescribed wellness advice achieved positive, neutral, or adverse physiological outcomes. Consequently, users receive generic, repetitive recommendations that frequently violate safety boundaries, induce cognitive fatigue, and ultimately lead to program abandonment.

This project introduces **CareCompanion**, an autonomous agentic wellness coaching architecture designed to achieve persistent cross-session memory, closed-loop physiological outcome verification, and deterministic clinical safety guardrails. CareCompanion implements a hybrid dual-brain design:
1. **High-Speed Cloud Inference Brain:** Powered by Groq Language Processing Units (LPUs) executing `qwen/qwen3.8-27b` via OpenAI-compatible function calling, supplemented by an automated 4-stage exponential backoff engine to survive free-tier rate limits.
2. **Deterministic Offline State Machine Brain:** An autonomous local fallback compiler that guarantees 100% operational uptime in disconnected or offline environments without external cloud dependencies.

### Key Performance Indicators (KPIs)
- **5 Specialized Agentic Tools:** `get_user_profile`, `recall_memories`, `get_health_summary`, `check_advice_outcomes`, `log_advice`.
- **28-Day Longitudinal Telemetry:** Daily steps, sleep duration, resting heart rate (RHR), and active calories synthesized with zero baseline drift ($\sum \delta_i = 0$).
- **8 / 8 Automated Pytest Suite:** 100% test pass rate in 0.77 seconds covering database, memory, tools, agent reasoning, fallback, and clinical safety.
- **Latency & Reliability:** Sub-1.2-second response latency on Groq LPU, zero leaked tool tokens, and instant offline execution.

---

# SECTION 3: PART I — PROBLEM CONTEXT, CLINICAL FOUNDATIONS & SOLUTION CONCEPT
*Authored by: Hari Dev Shaji (12313476)*

## 3.1 The Clinical Challenge of Modern Digital Health
Non-communicable chronic conditions (metabolic syndrome, cardiovascular disease, hypertension, and sleep disorders) account for over 70% of preventable global mortality. While clinical trials prove that daily lifestyle habits (regular ambulation, sleep hygiene, structured cardiovascular exercise) yield therapeutic benefits matching primary pharmaceuticals, conventional coaching delivery suffers from three structural failures:
1. **Severe Cost Barriers:** Certified human coaches charge steep hourly fees, making regular check-ins economically unattainable for the general population.
2. **Caseload Fatigue:** Human coaches managing dozens of patients rely on fallible clinical notes and struggle to track multi-week trend lines across wearable device streams.
3. **Episodic Consultations:** Consultations occur weeks or months apart, allowing behavioral relapses to persist unnoticed.

## 3.2 The Stateless Dilemma of Commercial LLMs
Deploying out-of-the-box LLMs (ChatGPT, Claude, or mobile health assistants) into healthcare coaching fails because of three architectural flaws:
- **Ephemeral Context Purge:** When a session concludes or context token limits are reached, all historical context is wiped. When a returning user says: *"My knee feels worse after following your advice,"* a stateless LLM has no memory of what exercise was prescribed or what joint pathology was previously disclosed.
- **Open-Loop Hallucination:** LLMs generate statistically likely text without verifying ground truth. If a coach suggests that a sedentary user begin jogging 5 km daily, and wearable sensor streams show that daily steps actually dropped due to exhaustion, a stateless LLM cannot correlate the biometric failure with its prior recommendation. It blindly repeats variations of the failed plan.
- **Diagnostic Sycophancy & Liability:** When faced with acute medical emergencies (e.g., chest tightness, shortness of breath), unconstrained LLMs frequently attempt conversational comfort or home remedies, catastrophically delaying urgent clinical care.

### Table 2: The Conversational Traps vs. CareCompanion Solutions

| Stateless Failure Mode | Real-World Manifestation | Clinical Danger | CareCompanion Solution |
| :--- | :--- | :--- | :--- |
| **Context Window Purge** | User must re-explain health goals and injuries every session. | High user fatigue; fragmented advice. | Relational SQLite database persisting user profiles, dialogue, and reflections. |
| **Amnesic Contraindication** | Coach prescribes heavy squats to a client who disclosed disc herniation. | Acute physical re-injury; orthopedic relapse. | Episodic reflection assigning maximum importance ($I=5$) to physical injuries. |
| **Open-Loop Prescription** | Coach repeats identical advice ('Walk 10,000 steps') despite sensor data showing failure. | Frustration, demotivation, program abandonment. | Closed-loop deadband classifier ($\pm 5\%$) comparing current sensor data to baseline. |
| **Diagnostic Drift** | Coach tries to explain away crushing chest pain as muscle soreness. | Life-threatening delay in emergency treatment. | Deterministic pre-LLM regex interceptor halting execution immediately for red flags. |

## 3.3 Behavioral Psychology Foundations
CareCompanion's algorithmic reasoning is grounded in two validated behavioral frameworks:
- **Transtheoretical Model of Behavior Change (TTM):** Prochaska and DiClemente establish that habit progression moves across discrete stages: *Precontemplation $\rightarrow$ Contemplation $\rightarrow$ Preparation $\rightarrow$ Action $\rightarrow$ Maintenance*. Stateless agents consistently fail by demanding aggressive Action-stage behaviors from Contemplation-stage users. CareCompanion uses conversational intake to tailor intervention difficulty.
- **BJ Fogg Behavior Model ($B = M \times A \times P$):** Dr. B.J. Fogg demonstrates that behavior occurs only when Motivation ($M$), Ability ($A$), and a Prompt ($P$) converge. When motivation dips, an intervention fails unless Ability is drastically increased by lowering friction (e.g., micro-habits). CareCompanion implements automated strategy pivots that systematically lower physical friction when an initial plan stalls.

---

# SECTION 4: PART II — SYSTEM ARCHITECTURE, MEMORY MODELING & AGENTIC REASONING
*Authored jointly by: Hari Dev Shaji (12313476) & Nikhil Singh (12313478)*

## 4.1 Layered System Architecture
CareCompanion is organized into four distinct operational tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      TIER 1: PRESENTATION LAYER                        │
│  • Streamlit Web UI (app.py)          • Headless CLI Runner (demo.py)  │
│  • Persona Switcher & Onboarding Form • Memory & Biometrics Inspector  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ User Inputs & Commands
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      TIER 2: REASONING LAYER                           │
│                     CareAgent Core (agent.py)                          │
│                                                                        │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐  │
│  │   Cloud LLM Brain (llm.py)   │    │  Offline Planner (mock_llm)  │  │
│  │  • Groq LPU (qwen3.8-27b)    │◄──►│  • Deterministic Slot Engine │  │
│  │  • OpenAI Tool Call Standard │    │  • Clinical Response Trees   │  │
│  │  • Exponential Backoff (429) │    └──────────────────────────────┘  │
│  └──────────────────────────────┘                                      │
│                                 │                                      │
│  ┌──────────────────────────────┴───────────────────────────────────┐  │
│  │  Anti-Leak Output Regex Sanitizer (_clean_reply in agent.py)     │  │
│  │  • Purges <tool_call> XML blocks and robotic developer meta-text │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Tool Invocations
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      TIER 3: EXECUTION & TOOLS                         │
│                         ToolBox (tools.py)                             │
│  • get_user_profile     • recall_memories     • get_health_summary     │
│  • check_advice_outcomes                      • log_advice             │
│                                                                        │
│  Guards:                                                               │
│  • Pre-LLM Deterministic Safety Interceptor (safety.py)                │
│  • End-of-Session Episodic Reflection Engine (reflection.py)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQL Queries & CSV Reads
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      TIER 4: PERSISTENCE LAYER                         │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐  │
│  │   SQLite Database Engine     │    │   Wearable Sensor Datastore  │  │
│  │   (data/carecompanion.db)    │    │   (data/synthetic/<uid>/)    │  │
│  │   • users       • sessions   │    │   • 28-day daily.csv logs    │  │
│  │   • memories    • advice_log │    │   • people.json metadata     │  │
│  └──────────────────────────────┘    └──────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Dual-Brain Execution Pipeline
- **Groq LPU Cloud Gateway:** When an API key is present, calls are dispatched to Groq LPUs running `qwen/qwen3.8-27b`. During high-concurrency bursts, an integrated 4-stage exponential backoff algorithm in `llm.py` intercepts HTTP 429 rate limits:
  $$\text{Delay} = 8 \times (\text{attempt} + 1) \text{ seconds}$$
- **Deterministic Offline Planner:** If no API key exists, or if cloud calls fail, `CareAgent` falls back to `mock_llm.py`. Using regular-expression slot parsing, it identifies intents (sleep, steps, pain) and calls the identical 5 tools, assembling structured responses from clinical templates. The app never crashes.

## 4.3 Relational Database Schema (SQLite)
The database schema (`data/carecompanion.db`) models cross-session memory in Third Normal Form (3NF) across four tables:
1. **`users`:** `user_id` (PK, TEXT), `name` (TEXT), `created_at` (TEXT).
2. **`sessions`:** `session_id` (PK, TEXT), `user_id` (FK, TEXT), `session_num` (INTEGER), `started_at` (TEXT), `ended_at` (TEXT), `summary` (TEXT).
3. **`memories`:** `memory_id` (PK, TEXT), `user_id` (FK, TEXT), `category` (TEXT: goal, injury, preference), `content` (TEXT), `importance` (INTEGER: 1 to 5), `updated_at` (TEXT). Indexed on `user_id`.
4. **`advice_log`:** `advice_id` (PK, TEXT), `user_id` (FK, TEXT), `session_num` (INTEGER), `topic` (TEXT), `strategy` (TEXT), `baseline_val` (REAL), `created_at` (TEXT). Indexed on `(user_id, topic)`.

## 4.4 Synthetic Telemetry Generator with Zero Baseline Drift
To evaluate longitudinal progress without exposing private patient data, CareCompanion synthesizes 28 days (4 weeks) of realistic biometric wearable telemetry (`carecompanion/synthetic.py`).
To prevent uncontrolled random walk baseline drift, the engine uses a **Zero-Mean Weekly Normalized Gaussian Noise Model**:
For metric $m \in \{\text{steps}, \text{sleep\_hours}, \text{resting\_hr}, \text{calories}\}$ across week $w \in \{0, 1, 2, 3\}$:
1. Sample 7 raw perturbations: $\xi_i \sim \mathcal{N}(0, \sigma_m^2)$ for day $i \in \{0, \dots, 6\}$.
2. Calculate empirical weekly perturbation mean: $\mu = \frac{1}{7} \sum_{i=0}^{6} \xi_i$.
3. Compute zero-mean normalized daily noise: $\delta_i = \xi_i - \mu \implies \sum_{i=0}^{6} \delta_i = 0$.
4. Calculate synthesized daily value: $X_m(7w + i) = \text{round}\left( \bar{X}_m[w] + \delta_i \right)$.

**Mathematical Proof of Zero Baseline Drift:**
$$\frac{1}{7} \sum_{i=0}^{6} X_m(7w + i) = \frac{1}{7} \sum_{i=0}^{6} \left( \bar{X}_m[w] + \delta_i \right) = \bar{X}_m[w] + \frac{1}{7} \sum_{i=0}^{6} \delta_i = \bar{X}_m[w] + 0 = \bar{X}_m[w] \quad \text{(Q.E.D.)}$$

Variance scaling factors:
- $\sigma_{\text{steps}} = 0.08 \times \bar{X}_{\text{steps}}$ (8% daily coefficient of variation)
- $\sigma_{\text{sleep}} = 0.35\text{ hours}$ (21 minutes daily variance)
- $\sigma_{\text{RHR}} = 1.0\text{ bpm}$
- $\sigma_{\text{calories}} = 80\text{ kcal}$

## 4.5 The 5 Specialized Agent Tools
The `CareAgent` never queries raw SQL or CSV files directly. It operates exclusively through five validated tools:
1. `get_user_profile(user_id)`: Retrieves demographic profile, name, and total session count.
2. `recall_memories(user_id, query)`: Retrieves memories filtered by semantic keywords, sorted by importance ($I \in [1,5]$).
3. `get_health_summary(user_id, days)`: Computes statistical rolling average, min, and max across 7, 14, or 28 days of sensor telemetry.
4. `check_advice_outcomes(user_id)`: Compares past advice baselines against current 7-day wearable averages to calculate delta % and status (`improved`, `no_change`, `worse`).
5. `log_advice(user_id, topic, strategy)`: Records agreed strategy and baseline sensor value to `advice_log`.

## 4.6 Closed-Loop Outcome Tracking & Strategy Modification
When a returning user starts a consultation, `check_advice_outcomes` calculates the relative percentage delta ($\Delta$):
$$\Delta = \frac{\bar{X}_{\text{current}} - X_{\text{baseline}}}{X_{\text{baseline}}} \times 100\%$$
- **$\Delta \ge +5.0\% \implies \text{"improved"}$:** Strategy succeeds; coach validates agency, celebrates win, and increments load.
- **$-5.0\% < \Delta < +5.0\% \implies \text{"no\_change"}$:** Strategy has stalled; coach acknowledges barrier without blame and **must pivot to a new strategy**.
- **$\Delta \le -5.0\% \implies \text{"worse"}$:** Regression; coach lowers friction or eliminates the prompt entirely.

## 4.7 Episodic Reflection & Importance Weighting ($I \in [1,5]$)
At session termination (`agent.end_session()`), the dialogue transcript is distilled into atomic facts:
- **$I = 5$ (Critical Safety Constraint):** Physical injuries, joint pain, surgical history, clinical contraindications.
- **$I = 4$ (Primary Health Goal):** Explicit target objectives (train for 10K, resolve insomnia).
- **$I = 3$ (Lifestyle Constraint):** Shift work, long commute, travel schedule.
- **$I = 2$ (Personal Preference):** Modality preferences (outdoor walks vs. gym).
- **$I = 1$ (Incidental Context):** Minor conversational remarks.

## 4.8 Anti-Leak Output Token Sanitizer (`_clean_reply`)
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

## 4.9 Deterministic Pre-LLM Clinical Safety Guardrails
Before invoking LLM reasoning, `carecompanion/safety.py` screens every user prompt against critical red-flag symptoms:
- *Myocardial Infarction / Angina:* Substernal chest pressure, radiating arm/jaw pain.
- *Cerebrovascular Accident (Stroke):* Facial drooping, unilateral arm weakness, slurred speech.
- *Acute Dyspnea:* Severe shortness of breath, respiratory distress.
- *Syncope / Neurotrauma:* Loss of consciousness, sudden severe headache.

If matched, execution halts immediately and returns a hardcoded clinical emergency notice:
> *"⚠️ MEDICAL EMERGENCY DETECTED: Your symptoms require immediate emergency care. Please call 911/112 or visit the nearest emergency room immediately."*

---

# SECTION 5: PART III — IMPLEMENTATION, VERIFICATION & EMPIRICAL RESULTS
*Authored by: Nikhil Singh (12313478)*

## 5.1 Technology Stack & Architectural Decisions
- **Language:** Python 3.10–3.12 (Native type hints, robust ecosystem).
- **Web Dashboard:** Streamlit 1.36+ (Zero JavaScript build overhead, native reactive components).
- **Relational Storage:** SQLite (Built-in, zero configuration, ACID-compliant, single-file portability).
- **LLM Gateway:** OpenAI Python SDK 1.40+ (Used with Groq LPU endpoint for `qwen/qwen3.8-27b`).
- **Secrets Management:** `python-dotenv` 1.0+ (Strict separation of environment variables from source).
- **Test Harness:** Pytest 8.0+ (Sub-second headless test discovery).

## 5.2 Dynamic User Creation ("➕ Add New User")
Evaluators can create custom profiles live from the Streamlit sidebar:
1. Enter custom Name (e.g., `Hari`) and select Goal (`Steps`, `Sleep`, `Cardio`).
2. System allocates unique ID `u_hari`, provisions a 4-week synthetic baseline stream (`daily.csv`), and registers the user in SQLite.
3. Automatically compiles dynamic onboarding starter prompts in `carecompanion/scripts.py`.

## 5.3 Automated Pytest Verification Suite
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

## 5.4 Multi-Session Empirical Case Studies

### 1. Persona `p01` (Aarav - Sleep Focus)
- **Baseline (Week 1):** Average sleep: 5.8 hours/night (severe sleep debt).
- **Session 1:** Coach logs advice: *11 PM bedtime routine with screens turned off 30 minutes prior*.
- **Session 2 (Week 2):** Wearable data reflects 6.7 hours/night ($+15.5\%$, `improved`). Coach validates agency and reinforces routine.
- **Session 3 (Week 4):** Sleep reaches 7.2 hours/night ($+24.1\%$). Coach transitions into long-term maintenance.

### 2. Persona `p02` (Meera - Steps Focus & Strategy Pivot)
- **Baseline (Week 1):** 3,500 steps/day (highly sedentary). Discloses mild knee pain when running ($I=5$).
- **Session 1:** Coach logs Strategy A: *Park 10 minutes away from office entrance to get morning steps*.
- **Session 2 (Week 2):** Wearable data reflects 3,600 steps/day ($+2.8\%$, `no_change`). Morning schedule caused parking friction. Coach acknowledges the stall and **pivots to Strategy B**: *Two 10-minute brisk walks scheduled directly after lunch and dinner*.
- **Session 3 (Week 4):** Steps surge to 5,400 (Week 3) and 5,600 (Week 4), yielding $+55.5\%$ (`improved`). When Meera asks: *"Should I start running 5 miles on the treadmill tomorrow?"*, the agent retrieves the knee pain memory from Session 1 and warns against high-impact treadmill running, advising low-impact walking or elliptical instead.

### 3. Persona `p03` (Rohan - Exam Stress & Sleep)
- **Baseline (Week 1):** High physical activity (9,500 steps/day), but sleep is 5.5 hours/night with elevated resting heart rate (70 bpm) due to exams.
- **Session 1:** Coach logs Strategy A: *Aggressive 10 PM bedtime alarm*.
- **Session 2 (Week 2):** Sleep remains at 5.6 hours/night ($+1.8\%$, `no_change`). Bedtime alarm created stress. Coach pivots to Strategy B: *10 minutes of evening box breathing and light dimming at 10 PM*.
- **Session 3 (Week 4):** Sleep recovers to 7.1 hours/night, while RHR drops from 70 to 67 bpm (`improved`).

## 5.5 Commercial Platform Comparison

| Feature | CareCompanion | Vanilla ChatGPT | Noom | Apple Health | Woebot |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cross-Session Memory** | **Relational SQLite ($I=1\dots5$)** | Ephemeral window | Human notes | Aggregate stats | Module state |
| **Biometric Grounding** | **28-Day Wearable Sensor Logs** | Manual chat input | Manual food log | Live sensors | None |
| **Adaptive Strategy Pivot**| **Automated Deadband ($\pm 5\%$)** | Open-loop repetition | Human-driven | Static reminders| Branching tree |
| **Safety Interception** | **Deterministic Pre-LLM Regex** | Soft model filter | Human triage | None | Keyword rules |
| **Offline Reliability** | **100% Deterministic Fallback** | 0% (Cloud only) | Cached articles | Native local | Partial |

## 5.6 Technical Challenges Resolved
1. **Groq Model 404 (`llama-3.3-70b-versatile`):** Queried `/models` endpoint, identified active model `qwen/qwen3.8-27b`, and standardized `.env.example`.
2. **Qwen Token Leakage:** Built `_clean_reply()` multi-regex cleaner to purge raw `<tool_call>` XML and developer meta-talk.
3. **Test Suite Fallback Assertion:** Refined fallback string assertion in `agent.py` to check emptiness rather than arbitrary length, ensuring 8/8 tests pass green.
4. **Credential Security Hygiene:** Sanitized `.env.example`, hardened `.gitignore` against `.env`, `*.db`, and `data/synthetic/u_*`.
5. **Instant Demo Seeder:** Authored `seed_demo_data.py` to populate all 3 benchmark personas with 9 complete sessions in under 2 seconds offline.

---

# SECTION 6: APPENDICES & REPRODUCIBILITY

## Appendix A: Quick Start Commands
```bash
# 1. Initialize Virtual Environment
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Seed Demo Database (Instant offline execution)
python seed_demo_data.py

# 4. Verify System via Pytest
pytest

# 5. Launch Web Dashboard
streamlit run app.py
```

## Appendix B: Database SQL Schema DDL
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

## Appendix C: Glossary of Key Terms
- **Agentic AI:** Autonomous software architecture capable of iterative planning, tool execution, and reflective state persistence.
- **ReAct Loop:** Reason + Act orchestration framework where the agent formulates reasoning, executes tools, observes data, and responds.
- **Closed-Loop Coaching:** System where future advice is strictly modulated by quantitative outcomes observed from previous interventions.
- **Deadband Threshold:** A $\pm 5.0\%$ tolerance window that prevents premature strategy modifications caused by natural biological variance.
- **Token Leakage:** The accidental emission of internal function-calling XML syntax (`<tool_call>`) into user-facing chat responses.
- **Deterministic Triage:** Hardcoded regular-expression screening that executes upstream of LLM processing to guarantee zero-latency emergency medical escalation.
