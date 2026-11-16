"""Run the 3-session demo (memory ON vs memory OFF) and write a report.

  python demo.py                      # person p02 (Meera), provider from .env
  python demo.py --user all           # all three people
  python demo.py --provider mock      # offline, no API key
"""
import argparse
import shutil
import time
from pathlib import Path

from carecompanion import config
from carecompanion.agent import CareAgent
from carecompanion.data_loader import DataStore
from carecompanion.db import Database
from carecompanion.llm import get_llm
from carecompanion.scripts import SCRIPTS
from carecompanion.synthetic import PEOPLE, ensure_data

OUT = config.ROOT / "demo_output"


def run_user(uid, llm, pause=0.0):
    store = DataStore()
    dbs, agents = {}, {}
    for mode in ("on", "off"):
        path = OUT / f"{uid}_memory_{mode}.db"
        path.unlink(missing_ok=True)
        dbs[mode] = Database(path)
        dbs[mode].ensure_user(uid, PEOPLE[uid]["name"])
        agents[mode] = CareAgent(dbs[mode], llm, store, uid, memory_enabled=(mode == "on"))
    md = [f"# CareCompanion demo: {PEOPLE[uid]['name']} ({uid})", f"_Model: {getattr(llm, 'label', llm.__class__.__name__)}_", "",
          f"**Data story:** {PEOPLE[uid]['story']}", ""]
    for s, messages in enumerate(SCRIPTS[uid], 1):
        for mode in ("on", "off"):
            agents[mode].start_session()
        sim = agents["on"].session["sim_date"]
        md += [f"## Session {s}  (Fitbit data up to {sim})", ""]
        for msg in messages:
            md += [f"**User:** {msg}", ""]
            for mode, title in (("on", "WITH memory"), ("off", "WITHOUT memory")):
                r = agents[mode].chat(msg)
                tools = ", ".join(t["tool"] for t in r["trace"]) or "none"
                md += [f"**CareCompanion ({title})**  \n_tools: {tools}_", "", r["reply"], ""]
                print(f"[{uid}] session {s} {mode}: {len(r['reply'])} chars, tools: {tools}")
                time.sleep(pause)
        end = agents["on"].end_session()
        agents["off"].end_session()
        md += [f"> **Memory saved after session {s}:** {end['summary']}", ""]
    md += ["## What the agent stored (memory ON)", "", "| Session | Type | Memory |", "|---|---|---|"]
    md += [f"| {m['session_no']} | {m['category']} | {m['content'][:140]} |" for m in dbs["on"].memories(uid)]
    md += ["", "## Advice tracker (did it work?)", "", "| Given in | Advice | Metric | Baseline | Later | Change | Outcome |", "|---|---|---|---|---|---|---|"]
    for a in dbs["on"].advice(uid):
        cur = "" if a["current"] is None else a["current"]
        chg = "" if a["change_pct"] is None else f"{a['change_pct']:+.1f}%"
        md.append(f"| S{a['session_no']} | {a['text'][:90]} | {a['metric']} | {a['baseline']} | {cur} | {chg} | **{a['status']}** |")
    report = OUT / f"report_{uid}.md"
    report.write_text("\n".join(md), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="p02", help="p01, p02, p03 or all")
    ap.add_argument("--provider", default=None, help="groq | azure | mock")
    ap.add_argument("--pause", type=float, default=0.0, help="seconds between calls (helps with rate limits)")
    a = ap.parse_args()
    ensure_data()
    OUT.mkdir(exist_ok=True)
    llm = get_llm(a.provider)
    for uid in (PEOPLE if a.user == "all" else [a.user]):
        print("Report:", run_user(uid, llm, a.pause))


if __name__ == "__main__":
    main()
