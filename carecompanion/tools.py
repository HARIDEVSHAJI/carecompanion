"""The agent's tools. Each tool is a plain Python function the LLM can call."""
import json

from .data_loader import HIGHER_IS_BETTER, TARGETS

METRIC_ENUM = ["steps", "sleep_hours", "resting_hr"]


def _fn(name, desc, props=None, required=None):
    return {"type": "function", "function": {"name": name, "description": desc,
            "parameters": {"type": "object", "properties": props or {}, "required": required or []}}}


SCHEMAS = {
    "get_health_summary": _fn("get_health_summary", "Fitbit averages (steps, sleep hours, resting HR, calories) for the "
                              "last N days vs the previous N days, plus targets.",
                              {"days": {"type": "integer", "description": "window size, default 7"}}),
    "get_user_profile": _fn("get_user_profile", "The user's name, session number, goals, constraints (injuries etc.) and preferences."),
    "recall_memories": _fn("recall_memories", "Search long-term memory from earlier sessions.",
                           {"query": {"type": "string"}, "limit": {"type": "integer"}}, ["query"]),
    "check_advice_outcomes": _fn("check_advice_outcomes", "Compare Fitbit data now against the baseline of advice given in "
                                 "earlier sessions: did it work (improved / no_change / worse)?"),
    "log_advice": _fn("log_advice", "Record a recommendation you are giving so its outcome can be checked next session.",
                      {"text": {"type": "string"}, "metric": {"type": "string", "enum": METRIC_ENUM},
                       "direction": {"type": "string", "enum": ["increase", "decrease"]},
                       "target": {"type": "number"}}, ["text", "metric"]),
    "save_memory": _fn("save_memory", "Store a durable fact about the user.",
                       {"category": {"type": "string", "enum": ["goal", "constraint", "preference", "progress", "context"]},
                        "content": {"type": "string"}, "importance": {"type": "integer"}}, ["category", "content"]),
}
MEMORY_TOOLS = {"get_user_profile", "recall_memories", "check_advice_outcomes", "log_advice", "save_memory"}


def classify(metric, baseline, current):
    pct = (current - baseline) / baseline * 100 if baseline else 0.0
    better = pct if HIGHER_IS_BETTER[metric] else -pct
    status = "improved" if better >= 5 else "worse" if better <= -5 else "no_change"
    return status, round(pct, 1)


class ToolBox:
    def __init__(self, db, mem, store, user_id, session, memory_enabled=True):
        self.db, self.mem, self.store = db, mem, store
        self.user_id, self.session, self.memory_enabled = user_id, session, memory_enabled

    def names(self):
        return [n for n in SCHEMAS if self.memory_enabled or n not in MEMORY_TOOLS]

    def schemas(self):
        return [SCHEMAS[n] for n in self.names()]

    def call(self, name, args=None) -> str:
        try:
            if isinstance(args, str):
                args = json.loads(args or "{}")
            if name not in self.names():
                return json.dumps({"error": f"tool '{name}' is not available"})
            return json.dumps(getattr(self, "t_" + name)(**(args or {})), default=str)
        except Exception as e:  # tools must never crash the agent
            return json.dumps({"error": f"{type(e).__name__}: {e}"})

    # ---- tools ----
    def t_get_health_summary(self, days=7, **_):
        return self.store.summary(self.user_id, self.session["sim_date"], max(1, min(int(days), 14)))

    def t_get_user_profile(self, **_):
        p = self.mem.profile()
        p.update({"name": self.db.user(self.user_id)["name"], "session_number": self.session["session_no"]})
        return p

    def t_recall_memories(self, query="", limit=5, **_):
        past = [m for m in self.mem.recall(query, int(limit)) if m["session_no"] <= self.session["session_no"]]
        return {"memories": [{"category": m["category"], "content": m["content"], "session_no": m["session_no"],
                              "importance": m["importance"]} for m in past]}

    def t_check_advice_outcomes(self, **_):
        sn = self.session["session_no"]
        cur = self.store.summary(self.user_id, self.session["sim_date"])["current"]
        for a in self.db.advice(self.user_id):
            if a["status"] == "open" and a["session_no"] < sn and cur.get(a["metric"]) is not None and a["baseline"]:
                status, pct = classify(a["metric"], a["baseline"], cur[a["metric"]])
                self.db.update_advice(a["id"], status, cur[a["metric"]], pct, sn)
        fmt = lambda a: {"advice": a["text"], "metric": a["metric"], "given_in_session": a["session_no"],
                         "baseline": a["baseline"], "current": a["current"], "change_pct": a["change_pct"],
                         "outcome": a["status"]}
        rows = [a for a in self.db.advice(self.user_id) if a["status"] != "open"]
        return {"evaluated_now": [fmt(a) for a in rows if a["outcome_session_no"] == sn],
                "earlier_history": [fmt(a) for a in rows if a["outcome_session_no"] != sn],
                "note": "outcome compares the 7-day average now with the 7-day average when advice was given"}

    def t_log_advice(self, text, metric, direction=None, target=None, **_):
        if metric not in TARGETS:
            return {"error": f"metric must be one of {METRIC_ENUM}"}
        for a in self.db.advice(self.user_id):
            if a["session_id"] == self.session["id"] and a["metric"] == metric:
                return {"status": "already_logged_this_session", "id": a["id"]}
        base = self.store.summary(self.user_id, self.session["sim_date"])["current"][metric]
        direction = direction or ("increase" if HIGHER_IS_BETTER[metric] else "decrease")
        aid = self.db.add_advice(self.user_id, self.session, text, metric, direction,
                                 target if target is not None else TARGETS[metric], base)
        return {"status": "logged", "id": aid, "baseline": base}

    def t_save_memory(self, category, content, importance=3, **_):
        ok = self.mem.add(self.session, category, content, importance)
        return {"status": "saved" if ok else "duplicate_ignored"}
