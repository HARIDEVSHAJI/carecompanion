"""Generates synthetic Fitbit-style data (4 weeks per person) with a designed story.

Weekly averages are exact (noise is zero-mean per week) so results are repeatable.
"""
import csv
import datetime as dt
import json
import random
from pathlib import Path

from . import config

PEOPLE = {
    "p01": {"name": "Aarav", "story": "Poor sleep at first; improves quickly once he follows the bedtime advice, steps stay low.",
            "steps": [4800, 4900, 5000, 5100], "sleep_hours": [5.8, 6.7, 7.1, 7.2],
            "resting_hr": [68, 67, 66, 66], "calories": [2100, 2120, 2130, 2150]},
    "p02": {"name": "Meera", "story": "Very low steps; the first tip does NOT work, the changed strategy does.",
            "steps": [3500, 3600, 5400, 5600], "sleep_hours": [7.2, 7.1, 7.3, 7.3],
            "resting_hr": [74, 74, 72, 72], "calories": [1900, 1900, 1950, 1980]},
    "p03": {"name": "Rohan", "story": "Active, but sleeps badly during exams; sleep fixes only after strategy change.",
            "steps": [9500, 9400, 9600, 9500], "sleep_hours": [5.5, 5.6, 6.9, 7.1],
            "resting_hr": [70, 70, 68, 67], "calories": [2600, 2580, 2600, 2620]},
}
SD = {"steps": 0.08, "sleep_hours": 0.35, "resting_hr": 1.0, "calories": 80}
START = dt.date(2024, 3, 4)  # a Monday


def _noise(rng, sd, base, n=7):
    sd = sd * base if sd < 1 and base > 100 else sd
    v = [rng.gauss(0, sd) for _ in range(n)]
    m = sum(v) / n
    return [x - m for x in v]


def generate(base=None, seed=7, weeks=4):
    base = Path(base) if base else config.DATA_DIR / "synthetic"
    rng = random.Random(seed)
    for uid, p in PEOPLE.items():
        d = base / uid
        d.mkdir(parents=True, exist_ok=True)
        rows = []
        for w in range(weeks):
            noise = {m: _noise(rng, SD[m], p[m][w]) for m in SD}
            for i in range(7):
                day = START + dt.timedelta(days=7 * w + i)
                rows.append({"date": day.isoformat(),
                             "steps": round(p["steps"][w] + noise["steps"][i]),
                             "sleep_hours": round(p["sleep_hours"][w] + noise["sleep_hours"][i], 2),
                             "resting_hr": round(p["resting_hr"][w] + noise["resting_hr"][i], 1),
                             "calories": round(p["calories"][w] + noise["calories"][i])})
        with open(d / "daily.csv", "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=["date", "steps", "sleep_hours", "resting_hr", "calories"])
            wr.writeheader()
            wr.writerows(rows)
    (base / "people.json").write_text(json.dumps({k: {"name": v["name"], "story": v["story"]} for k, v in PEOPLE.items()}, indent=2))
    return base


def ensure_data():
    base = config.DATA_DIR / "synthetic"
    if not all((base / u / "daily.csv").exists() for u in PEOPLE):
        generate(base)
    return base


def get_all_people(base=None):
    base = Path(base) if base else config.DATA_DIR / "synthetic"
    people = dict(PEOPLE)
    custom_file = base / "custom_users.json"
    if custom_file.exists():
        try:
            with open(custom_file, "r", encoding="utf-8") as f:
                custom = json.load(f)
                people.update(custom)
        except Exception:
            pass
    return people


def create_new_user(name: str, goal: str = "steps", base=None):
    base = Path(base) if base else config.DATA_DIR / "synthetic"
    existing = get_all_people(base)
    clean_name = "".join(c for c in name.lower() if c.isalnum()) or "user"
    uid = f"u_{clean_name}"
    counter = 1
    while uid in existing:
        uid = f"u_{clean_name}_{counter}"
        counter += 1

    goal_lower = goal.lower()
    if "sleep" in goal_lower:
        story = "New user focusing on improving sleep quality and building healthy evening habits."
        steps_curve = [5200, 5300, 5600, 5800]
        sleep_curve = [5.4, 5.8, 6.7, 7.1]
        hr_curve = [72, 71, 69, 68]
        cal_curve = [2050, 2080, 2120, 2150]
    elif any(k in goal_lower for k in ("heart", "cardio", "rate", "fitness")):
        story = "New user working on cardiovascular endurance and lowering resting heart rate."
        steps_curve = [5000, 5400, 6200, 7100]
        sleep_curve = [6.5, 6.6, 6.8, 7.0]
        hr_curve = [78, 76, 72, 69]
        cal_curve = [2150, 2200, 2300, 2400]
    else:  # steps / weight loss / activity
        story = "New user aiming to increase daily movement, build active routines, and hit 7,000+ steps."
        steps_curve = [3600, 4100, 5500, 6800]
        sleep_curve = [6.8, 6.9, 7.0, 7.1]
        hr_curve = [74, 73, 71, 70]
        cal_curve = [1900, 1940, 2020, 2120]

    user_info = {
        "name": name.strip(),
        "story": story,
        "goal": goal,
        "steps": steps_curve,
        "sleep_hours": sleep_curve,
        "resting_hr": hr_curve,
        "calories": cal_curve
    }

    d = base / uid
    d.mkdir(parents=True, exist_ok=True)
    rng = random.Random()
    rows = []
    weeks = 4
    for w in range(weeks):
        noise = {m: _noise(rng, SD[m], user_info[m][w]) for m in SD}
        for i in range(7):
            day = START + dt.timedelta(days=7 * w + i)
            rows.append({
                "date": day.isoformat(),
                "steps": round(user_info["steps"][w] + noise["steps"][i]),
                "sleep_hours": round(user_info["sleep_hours"][w] + noise["sleep_hours"][i], 2),
                "resting_hr": round(user_info["resting_hr"][w] + noise["resting_hr"][i], 1),
                "calories": round(user_info["calories"][w] + noise["calories"][i])
            })
    with open(d / "daily.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["date", "steps", "sleep_hours", "resting_hr", "calories"])
        wr.writeheader()
        wr.writerows(rows)

    custom_file = base / "custom_users.json"
    custom_data = {}
    if custom_file.exists():
        try:
            with open(custom_file, "r", encoding="utf-8") as f:
                custom_data = json.load(f)
        except Exception:
            pass
    custom_data[uid] = user_info
    custom_file.write_text(json.dumps(custom_data, indent=2), encoding="utf-8")

    return uid, user_info

