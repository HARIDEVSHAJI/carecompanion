"""A rule-based stand-in for the LLM so the whole project runs offline (no API key).

It follows the same protocol as the real model: it calls tools, reads the results, and writes
a reply. It is deliberately simple; the real LLM (Groq/Azure) writes much more natural answers.
"""
import json

from .data_loader import HIGHER_IS_BETTER, TARGETS, gap_pct
from .memory import to_second_person

LABEL = {"steps": "daily steps", "sleep_hours": "sleep", "resting_hr": "resting heart rate"}
TACTICS = {
    "sleep_hours": [
        "Pick a fixed bedtime 30 minutes earlier than your current one and keep your phone away from the bed.",
        "Add a 20-minute wind-down: no screens, dim lights, light stretching or reading, and keep the same wake-up time every day, weekends included.",
        "Cut caffeine after 2 pm, avoid heavy meals within 3 hours of bed, and get 10 minutes of morning daylight to anchor your body clock."],
    "steps": [
        "Add one 15-minute walk {time} every day.",
        "Make walking automatic: set two phone reminders and attach a short walk to something you already do (a phone call or tea break). Aim for 3 walks of 10 minutes.",
        "Raise your daily target step by step: add 1,000 steps to last week's average, and invite a friend to walk with you so it's harder to skip."],
    "resting_hr": [
        "Do three easy, conversational-pace sessions of 25-30 minutes this week ({activity}).",
        "Keep the three easy sessions and add one short interval day (1 minute a bit harder, 2 minutes easy, repeated 5 times), plus 5 minutes of slow breathing before bed.",
        "Build up to 4 easy sessions a week and keep your sleep consistent, because poor sleep keeps resting heart rate high."],
}
BOOST = {"sleep_hours": ("sleep", "rest", "tired", "energy"), "steps": ("walk", "active", "weight", "steps", "fitness", "fitter"),
         "resting_hr": ("heart", "cardio", "fitness")}
ACTIVITIES = ["cycling", "swimming", "walking", "yoga", "dancing", "running", "jogging"]
CONTEXT_TOOLS = {"get_user_profile", "recall_memories", "get_health_summary", "check_advice_outcomes"}


def fmt(metric, v):
    return f"{v:,.0f}" if metric == "steps" else f"{v:.1f} h" if metric == "sleep_hours" else f"{v:.0f} bpm"


def tactic(metric, tier, prefs, cons):
    p, c = " ".join(prefs).lower(), " ".join(cons).lower()
    time = "in the evening" if "evening" in p else "in the morning" if "morning" in p else "after lunch"
    act = next((a for a in ACTIVITIES if a in p and not (a in ("running", "jogging") and ("run" in c or "knee" in c))), "brisk walking")
    ladder = TACTICS[metric]
    t = ladder[min(tier, len(ladder) - 1)].format(time=time, activity=act)
    if metric != "sleep_hours" and any(k in c for k in ("knee", "joint", "back", "pain", "injur")):
        t += " Keep it low-impact (no running or jumping) because of the pain you told me about."
    return t


def make_plan(res):
    prof, summ, outs = res.get("get_user_profile") or {}, res.get("get_health_summary") or {}, res.get("check_advice_outcomes") or {}
    cur = summ.get("current", {})
    goals, prefs, cons = " ".join(prof.get("goals", [])).lower(), prof.get("preferences", []), prof.get("constraints", [])
    now = outs.get("evaluated_now", [])
    counts = {}
    for h in now + outs.get("earlier_history", []):
        counts[h["metric"]] = counts.get(h["metric"], 0) + 1
    chosen = [(o["metric"], "escalate") for o in now if o["outcome"] != "improved"][:2]
    if not chosen:
        best, best_score = None, 0
        for m in TARGETS:
            if cur.get(m) is None:
                continue
            g = gap_pct(m, cur[m])
            score = g * (2 if any(k in goals for k in BOOST[m]) else 1)
            if g >= 3 and score > best_score:
                best, best_score = m, score
        if best:
            chosen = [(best, "progress" if counts.get(best) else "new")]
    return [{"metric": m, "kind": k, "direction": "increase" if HIGHER_IS_BETTER[m] else "decrease",
             "target": TARGETS[m], "text": tactic(m, counts.get(m, 0), prefs, cons)} for m, k in chosen]


def compose_first(res, plan):
    prof, summ, outs = res.get("get_user_profile"), res.get("get_health_summary") or {}, res.get("check_advice_outcomes") or {}
    parts = []
    if prof:
        n, name = prof["session_number"], prof["name"]
        parts.append(f"Hi {name}! Nice to meet you. I'm your health coach, and I'll remember what you tell me and check whether my advice actually works." if n == 1
                     else f"Welcome back, {name}! This is session {n}.")
        known = [to_second_person(x) for x in prof["goals"] + prof["constraints"] + prof["preferences"]]
        if known:
            parts.append(("Here's what I understood from you: " if n == 1 else "Here's what I remember about you: ") + "; ".join(known) + ".")
        for o in outs.get("evaluated_now", []):
            lab, b, c = LABEL[o["metric"]], fmt(o["metric"], o["baseline"]), fmt(o["metric"], o["current"])
            if o["outcome"] == "improved":
                parts.append(f"Last time I suggested: \"{o['advice']}\" Your {lab} moved from {b} to {c} ({o['change_pct']:+.0f}%). That worked, great job!")
            else:
                parts.append(f"Last time I suggested: \"{o['advice']}\" Your {lab} went from {b} to {c} ({o['change_pct']:+.0f}%), so it didn't really work for you. I won't repeat it; let's change the approach.")
    else:
        parts.append("Hi! Here's some general guidance based on your recent activity.")
    c = summ.get("current", {})
    if c.get("steps") is not None:
        parts.append(f"Your last 7 days: about {fmt('steps', c['steps'])} steps/day, {fmt('sleep_hours', c['sleep_hours'])} sleep, resting heart rate {fmt('resting_hr', c['resting_hr'])}.")
    if plan:
        lead = {"escalate": "New approach", "progress": "Building on your progress", "new": "This week's focus"}
        parts.append("\n".join(f"**{lead[p['kind']] if prof else 'Suggestion'} ({LABEL[p['metric']]}):** {p['text']}" for p in plan))
    else:
        parts.append("You're meeting your targets. Keep your current routine!")
    parts.append("Does that feel doable? Tell me what gets in the way and I'll adapt." if prof else "Tell me about your goals and I can tailor this.")
    return "\n\n".join(parts)


def compose_followup(user_text, res, logged):
    parts = ["Thanks for telling me that."]
    keep = [m for m in (res.get("recall_memories") or {}).get("memories", []) if m["category"] in ("constraint", "goal", "preference")]
    if keep:
        parts.append(f"I'm keeping in mind that {to_second_person(keep[0]['content'])}.")
    if "desk" in user_text.lower():
        parts.append("A simple desk option: stand up and walk for 2 minutes every hour, with a few shoulder rolls and calf raises.")
    if logged:
        parts.append(f"Let's stick with this week's plan: {logged[0]}")
        parts.append("I'll check your Fitbit data next session to see whether it worked.")
    else:
        parts.append("Small, consistent habits usually beat big changes. Which part of your day is easiest to adjust?")
    return "\n\n".join(parts)


class MockLLM:
    is_mock = True
    label = "mock (offline rule-based)"

    def chat(self, messages, tools=None, temperature=0):
        names = {t["function"]["name"] for t in (tools or [])}
        user_idx = max(i for i, m in enumerate(messages) if m["role"] == "user")
        user_text = messages[user_idx]["content"]
        first = sum(m["role"] == "user" for m in messages) == 1
        calls, res = {}, {}
        for m in messages[user_idx + 1:]:
            for c in m.get("tool_calls") or []:
                calls[c["id"]] = c["function"]["name"]
            if m["role"] == "tool":
                res[calls.get(m["tool_call_id"], "?")] = json.loads(m["content"])
        logged = [json.loads(c["function"]["arguments"])["text"] for m in messages if m["role"] == "assistant"
                  for c in (m.get("tool_calls") or []) if c["function"]["name"] == "log_advice"]

        def tool_msg(items):
            return {"content": "", "tool_calls": [{"id": f"call_{len(messages)}_{i}", "name": n, "arguments": json.dumps(a)}
                                                  for i, (n, a) in enumerate(items)]}

        if not (set(res) & CONTEXT_TOOLS):
            want = [("get_user_profile", {}), ("recall_memories", {"query": user_text}), ("get_health_summary", {}),
                    ("check_advice_outcomes", {})] if first else [("recall_memories", {"query": user_text})]
            want = [w for w in want if w[0] in names]
            if want:
                return tool_msg(want)
        if first:
            plan = make_plan(res)
            if "log_advice" in names and "log_advice" not in res and plan:
                return tool_msg([("log_advice", {k: p[k] for k in ("text", "metric", "direction", "target")}) for p in plan])
            return {"content": compose_first(res, plan), "tool_calls": []}
        return {"content": compose_followup(user_text, res, logged), "tool_calls": []}
