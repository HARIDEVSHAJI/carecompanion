"""Basic safety: detect red-flag messages and answer with a 'see a professional' message."""
import re

RED_FLAGS = [r"chest (pain|pressure|tightness)", r"(can'?t|cannot|trouble|difficulty) breath", r"short(ness)? of breath",
             r"faint(ed|ing)", r"passed out", r"\bstroke\b", r"heart attack", r"suicid", r"kill myself",
             r"self[- ]harm", r"severe (pain|bleeding)", r"vomiting blood", r"numb(ness)? (in|on) (my )?(arm|face|left)"]

EMERGENCY_REPLY = (
    "I'm worried about what you just described, and this could be serious. I can't assess it, so please "
    "contact your local emergency number now (112 in India, 911 in the US, 999 in the UK) or get to the nearest "
    "emergency department, or call a doctor right away. If you are having thoughts of harming yourself, please "
    "reach out to a crisis line or someone you trust right now. I'm here to keep coaching once you're safe."
)
DISCLAIMER = "\n\n_General wellness guidance only, not medical advice. Talk to a doctor about health concerns._"


def check_red_flags(text: str):
    return EMERGENCY_REPLY if any(re.search(p, text or "", re.I) for p in RED_FLAGS) else None
