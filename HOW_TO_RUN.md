# 🚀 How to Run & Deploy CareCompanion

Welcome to **CareCompanion** — an agentic AI health and wellness coach featuring persistent multi-session memory, biometric outcome tracking, and adaptive habit coaching.

This guide walks you through setting up, running locally, and deploying the application.

---

## 📋 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Local Setup (Step-by-Step)](#2-local-setup-step-by-step)
3. [Running the Application](#3-running-the-application)
4. [Setting Up AI API Keys (Optional but Recommended)](#4-setting-up-ai-api-keys-optional-but-recommended)
5. [Testing the Project](#5-testing-the-project)
6. [Cloud Deployment (Streamlit Community Cloud & Render)](#6-cloud-deployment)
7. [Troubleshooting & FAQs](#7-troubleshooting--faqs)

---

## 1. Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12 installed.
  - Download from [python.org](https://www.python.org/downloads/).
  - **Important on Windows**: Ensure you check the box **"Add Python to PATH"** during installation.
- **Git** (optional, for version control / GitHub deployment).

---

## 2. Local Setup (Step-by-Step)

### Step 2.1: Open Terminal in the Project Folder
Open PowerShell, Command Prompt, or your terminal inside this folder:
```bash
# Verify python is available
python --version
```

### Step 2.2: Create a Virtual Environment
Isolating dependencies ensures a clean install without conflicts:

**On Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(Your terminal prompt should now show `(.venv)` at the beginning).*

### Step 2.3: Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2.4: Seed the Demo Database (Instant)
Before launching the app, generate synthetic benchmark data and pre-seed initial demo history for Aarav, Meera, and Rohan:
```bash
python seed_demo_data.py
```
*This command runs completely offline and sets up `data/carecompanion.db` in seconds.*

---

## 3. Running the Application

### Option A: Interactive Web UI (Streamlit)
Launch the full web dashboard in your browser:
```bash
streamlit run app.py
```
- Your browser will automatically open to `http://localhost:8501`.
- **What you will see:**
  - **Sidebar:** Choose a persona (Aarav, Meera, Rohan) or click **"➕ Add New User"** to create a custom profile.
  - **Main Screen:** Biometric analytics (Steps, Sleep, Resting Heart Rate), Persistent Memory inspector, and live multi-session chat with the AI coach.
  - **Interactive Buttons:** Pre-scripted prompts to demonstrate Session 1 vs. Session 2 vs. Session 3 adaptive memory recall.

### Option B: Headless Terminal Comparison (CLI Demo)
To see an automated side-by-side comparison of **Memory ON vs. Memory OFF** across 3 simulated sessions:
```bash
python demo.py --user p02
```
*Generates an analysis report in `demo_output/report_p02.md` showing how advice adapts over time.*

---

## 4. Setting Up AI API Keys (Optional but Recommended)

By default, CareCompanion runs with a **built-in offline mock coach** that requires zero API keys and zero internet access.

To connect real LLMs:

### Step 4.1: Create your `.env` file
Make a copy of `.env.example` named `.env`:
- **Windows (PowerShell):** `Copy-Item .env.example .env`
- **macOS / Linux:** `cp .env.example .env`

### Step 4.2: Add a Free Groq API Key
1. Sign up for free at [console.groq.com/keys](https://console.groq.com/keys).
2. Generate an API Key (starts with `gsk_...`).
3. Open `.env` in any text editor and update:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your_actual_key_here
   GROQ_MODEL=qwen/qwen3.8-27b
   ```

### Step 4.3: Verify Connection
Run the connection checker:
```bash
python check_connection.py
```
You should see: `✓ Connection successful! Model answered: ...` and `✓ Tool calling works!`.

---

## 5. Testing the Project

To verify that all components, database routines, and safety guardrails are functioning properly:
```bash
pytest
```
*All 8 unit and integration tests should pass.*

---

## 6. Cloud Deployment

### Method 1: Deploy on Streamlit Community Cloud (Recommended & Free)
1. Push this folder to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of CareCompanion"
   git branch -M main
   git remote add origin https://github.com/<your-username>/carecompanion.git
   git push -u origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **"New app"**:
   - **Repository:** `<your-username>/carecompanion`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. In **Advanced Settings -> Secrets**, add your environment variables:
   ```toml
   LLM_PROVIDER = "groq"
   GROQ_API_KEY = "gsk_..."
   GROQ_MODEL = "qwen/qwen3.8-27b"
   ```
5. Click **Deploy!** Your app will be live on a public URL in 1-2 minutes.

---

### Method 2: Deploy on Render / Railway / Cloud Run
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- **Environment Variables:**
  - `LLM_PROVIDER`: `groq`
  - `GROQ_API_KEY`: `gsk_...`
  - `GROQ_MODEL`: `qwen/qwen3.8-27b`

---

## 7. Troubleshooting & FAQs

- **Q: Do I need a credit card or paid API to run this?**
  - **No.** The project runs 100% free out of the box using offline mock mode, or using Groq's generous free tier (`qwen/qwen3.8-27b`).
- **Q: Where is data stored?**
  - SQLite database is saved automatically to `data/carecompanion.db`.
  - Synthetic biometric datasets reside in `data/synthetic/`.
- **Q: Can I reset the database back to clean demo state?**
  - Yes! Just run `python seed_demo_data.py`.
- **Q: `streamlit: command not found`?**
  - Make sure your virtual environment is activated (`.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Unix).

