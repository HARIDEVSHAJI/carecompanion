"""End-of-session reflection: turn a conversation into a summary + durable memories."""
import json
import re

from .memory import to_second_person

GREETING = re.compile(r"^(hi|hello|hey)( again| there)?\b[,!\s]*", re.I)
INTRO = re.compile(r"^(i'?m|i am|my name is)\s+\w+$", re.I)
PATTERNS = [
    ("goal", 5, re.compile(r"\b(want|goal|trying to|hope to|would like)\b", re.I)),
    ("constraint", 5, re.compile(r"\b(pain|injur\w*|can'?t|cannot|allerg\w*|avoid|asthma|diabet\w*)\b", re.I)),
    ("preference", 3, re.compile(r"\b(prefer|love|enjoy|like to|hate)\b", re.I)),
    ("progress", 3, re.compile(r"\b(tried|managed|did|didn'?t|skipped|forgot|forget|stick|stuck|felt|feel|feeling|worked)\b", re.I)),
]


def heuristic_reflect(user_texts, session_no, advice_texts):
    """Offline (rule-based) version, used by mock mode and as a fallback if the LLM fails."""
    mems = []
    for text in user_texts:
        for sent in re.split(r"[.!?\n]+", text):
            sent = GREETING.sub("", sent.strip()).strip(" ,")
            if len(sent.split()) < 4 or INTRO.match(sent):
                continue
            for cat, imp, rx in PATTERNS:
                if rx.search(sent):
                    mems.append({"category": cat, "content": sent, "importance": imp})
                    break
            else:
                mems.append({"category": "context", "content": sent, "importance": 2})
    said = "; ".join(to_second_person(m["content"]) for m in sorted(mems, key=lambda m: -m["importance"])[:3])
    adv = "; ".join(a[:90] for a in advice_texts)
    summary = f"Session {session_no}: user said {said or 'little'}." + (f" Advice given: {adv}." if adv else "")
    return {"summary": summary[:500], "memories": mems}


REFLECT_PROMPT = """You are the memory module of a health coach. Read the conversation and return ONLY JSON:
{"summary": "2-3 sentence summary of the session (what the user shared, what advice was given)",
 "memories": [{"category": "goal|constraint|preference|progress|context", "content": "short fact in third person or first person", "importance": 1-5}]}
Only include DURABLE facts (goals, injuries/limits, preferences, what they tried and how it went). Max 6 memories. No medical diagnoses."""


def llm_reflect(llm, transcript, advice_texts):
    msgs = [{"role": "system", "content": REFLECT_PROMPT},
            {"role": "user", "content": transcript + "\n\nAdvice logged this session: " + "; ".join(advice_texts)}]
    raw = llm.chat(msgs, tools=None, temperature=0)["content"]
    data = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    cats = {"goal", "constraint", "preference", "progress", "context"}
    mems = [{"category": m["category"] if m.get("category") in cats else "context", "content": str(m["content"]),
             "importance": max(1, min(5, int(m.get("importance", 3))))} for m in data.get("memories", [])[:6]]
    return {"summary": str(data["summary"])[:600], "memories": mems}
