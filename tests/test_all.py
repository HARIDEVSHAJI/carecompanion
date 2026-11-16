import datetime as dt

import pytest

from carecompanion.agent import CareAgent
from carecompanion.data_loader import DataStore
from carecompanion.db import Database
from carecompanion.memory import Memory
from carecompanion.mock_llm import MockLLM
from carecompanion.safety import check_red_flags
from carecompanion.scripts import SCRIPTS
from carecompanion.synthetic import PEOPLE, generate
from carecompanion.tools import classify


@pytest.fixture()
def env(tmp_path):
    base = tmp_path / "data"
    generate(base / "synthetic")
    return DataStore(base), tmp_path


def run(env, uid, memory=True):
    store, tmp = env
    db = Database(tmp / f"{uid}_{memory}.db")
    db.ensure_user(uid, PEOPLE[uid]["name"])
    agent = CareAgent(db, MockLLM(), store, uid, memory_enabled=memory)
    replies = []
    for msgs in SCRIPTS[uid]:
        agent.start_session()
        replies.append([agent.chat(m) for m in msgs])
        agent.end_session()
    return db, replies


def test_data_weekly_means_exact(env):
    store, _ = env
    s = store.summary("p02", dt.date(2024, 3, 10))
    assert abs(s["current"]["steps"] - 3500) < 2 and abs(s["current"]["sleep_hours"] - 7.2) < 0.02


def test_classify():
    assert classify("sleep_hours", 5.8, 6.7)[0] == "improved"
    assert classify("steps", 3500, 3600)[0] == "no_change"
    assert classify("resting_hr", 70, 60)[0] == "improved"  # lower HR is better
    assert classify("steps", 5000, 4000)[0] == "worse"


def test_memory_recall(env):
    store, tmp = env
    db = Database(tmp / "m.db")
    db.ensure_user("p02", "Meera")
    sess = db.new_session("p02", dt.date(2024, 3, 10))
    mem = Memory(db, "p02")
    mem.add(sess, "constraint", "I have knee pain so I can't run", 5)
    mem.add(sess, "preference", "I enjoy swimming", 3)
    assert not mem.add(sess, "preference", "I enjoy swimming", 3)  # duplicate ignored
    assert "knee" in mem.recall("my knee hurts", 1)[0]["content"]


def test_safety():
    assert check_red_flags("I have chest pain when I walk")
    assert not check_red_flags("I can't run because of my knee")


def test_p02_advice_adapts(env):
    db, rep = run(env, "p02")
    s1, s2, s3 = (r[0]["reply"] for r in rep)
    adv = db.advice("p02")
    assert [a["status"] for a in adv][:2] == ["no_change", "improved"]
    assert "didn't really work" in s2 and "worked" in s3
    assert "knee" in s1 and "low-impact" in s1
    assert adv[0]["text"] != adv[1]["text"]  # strategy changed after the tip failed
    assert "evening" in adv[0]["text"]  # personalised from a remembered preference


def test_p01_and_p03_flow(env):
    db, rep = run(env, "p01")
    assert db.advice("p01")[0]["status"] == "improved" and db.advice("p01")[0]["metric"] == "sleep_hours"
    assert "Welcome back" in rep[1][0]["reply"]
    db3, rep3 = run(env, "p03")
    assert [a["status"] for a in db3.advice("p03")][:2] == ["no_change", "improved"]
    assert "cycling" in db3.advice("p03")[-1]["text"]


def test_memory_off_is_generic(env):
    db, rep = run(env, "p02", memory=False)
    assert db.advice("p02") == [] and db.memories("p02") == []
    assert "Welcome back" not in rep[1][0]["reply"] and "remember" not in rep[2][0]["reply"].lower().replace("remember what", "")
    assert rep[1][0]["reply"].split("**")[1] == rep[2][0]["reply"].split("**")[1]  # same generic advice every session


def test_agent_survives_llm_failure(env):
    store, tmp = env
    class Broken(MockLLM):
        calls = 0
        def chat(self, messages, tools=None, temperature=0):
            Broken.calls += 1
            if tools:
                raise RuntimeError("tool_use_failed")
            return {"content": "fallback answer", "tool_calls": []}
    db = Database(tmp / "b.db"); db.ensure_user("p01", "Aarav")
    a = CareAgent(db, Broken(), store, "p01"); a.start_session()
    r = a.chat("hello there")
    assert "fallback answer" in r["reply"]
