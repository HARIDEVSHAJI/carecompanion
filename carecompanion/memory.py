"""Long-term memory: store facts, recall the most relevant ones, build a profile."""
import re

STOP = set("the and for are but not you your with that this have has was were from they them what when "
           "will can about just like get got its into out how why who all any one our his her she him".split())


def tokens(text: str) -> set:
    return {w for w in re.findall(r"[a-z]+", (text or "").lower()) if len(w) > 2 and w not in STOP}


def to_second_person(s: str) -> str:
    """'I want to sleep better' -> 'you want to sleep better' (for friendly recaps)."""
    s = re.sub(r"\bI am\b", "you are", s)
    s = re.sub(r"\bI was\b", "you were", s)
    for a, b in ((r"\bI'm\b", "you're"), (r"\bI've\b", "you've"), (r"\bI'd\b", "you'd"), (r"\bI'll\b", "you'll"),
                 (r"\bI\b", "you"), (r"\bmyself\b", "yourself"), (r"\bme\b", "you")):
        s = re.sub(a, b, s)
    s = re.sub(r"\bmy\b", "your", s, flags=re.I)
    return s.strip().rstrip(".")


class Memory:
    def __init__(self, db, user_id):
        self.db, self.user_id = db, user_id

    def add(self, session, category, content, importance=3) -> bool:
        content = (content or "").strip()
        if not content:
            return False
        if any(m["content"].lower() == content.lower() for m in self.db.memories(self.user_id)):
            return False  # no duplicates
        self.db.add_memory(self.user_id, session, category, content, int(importance))
        return True

    def all(self):
        return self.db.memories(self.user_id)

    def recall(self, query: str, limit: int = 5):
        """Rank memories by keyword overlap with the query + importance + recency."""
        q = tokens(query)
        scored = []
        for m in self.all():
            overlap = len(q & tokens(m["content"] + " " + m["category"]))
            scored.append((overlap * 3 + m["importance"] + m["session_no"] * 0.1, m))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [m for _, m in scored[:limit]]

    def profile(self) -> dict:
        mem = self.all()
        pick = lambda cat: [m["content"] for m in mem if m["category"] == cat]
        return {"goals": pick("goal"), "constraints": pick("constraint"), "preferences": pick("preference")}
