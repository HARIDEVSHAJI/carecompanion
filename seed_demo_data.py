"""Seed initial multi-session demo history for Aarav, Meera, and Rohan.

Usage:
  python seed_demo_data.py          # Runs offline with mock engine (instant)
  python seed_demo_data.py groq     # Uses Groq LLM from .env
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from carecompanion import config
from carecompanion.agent import CareAgent
from carecompanion.data_loader import DataStore
from carecompanion.db import Database
from carecompanion.llm import get_llm
from carecompanion.scripts import SCRIPTS
from carecompanion.synthetic import PEOPLE, ensure_data


def seed(provider="mock"):
    ensure_data()
    db = Database(config.DB_PATH)
    store = DataStore()
    llm = get_llm(provider)
    print(f"Seeding demo database using {getattr(llm, 'label', 'mock')}...")

    for uid, p in PEOPLE.items():
        db.reset_user(uid)
        db.ensure_user(uid, p["name"])
        agent = CareAgent(db, llm, store, uid, memory_enabled=True)
        print(f"Generating 3 sessions for {p['name']} ({uid})...")
        for s_idx, msgs in enumerate(SCRIPTS[uid], 1):
            agent.start_session()
            for m in msgs:
                agent.chat(m)
            agent.end_session()
        print(f"  ✓ {p['name']}: {db.session_count(uid)} sessions, {len(db.memories(uid))} memories, {len(db.advice(uid))} advice logged.")

    print("\nDatabase seeded successfully! You can now run: streamlit run app.py")


if __name__ == "__main__":
    prov = sys.argv[1] if len(sys.argv) > 1 else "mock"
    seed(prov)

