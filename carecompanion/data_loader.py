"""Fitbit-style health data. Reads synthetic CSVs or real PMData JSON folders."""
import csv
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

from . import config

METRICS = ("steps", "sleep_hours", "resting_hr", "calories")
TARGETS = {"steps": 7000.0, "sleep_hours": 7.0, "resting_hr": 65.0}
HIGHER_IS_BETTER = {"steps": True, "sleep_hours": True, "resting_hr": False}


def gap_pct(metric: str, value: float) -> float:
    """How far (in %) the value is from its target, in the 'bad' direction. 0 if target met."""
    t = TARGETS[metric]
    g = (t - value) / t if HIGHER_IS_BETTER[metric] else (value - t) / t
    return max(0.0, g * 100)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _load_csv(path: Path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            row = {"date": dt.date.fromisoformat(r["date"])}
            row.update({m: _num(r.get(m)) for m in METRICS})
            rows.append(row)
    return rows


def _day(s):
    for fmt in ("%m/%d/%y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def _load_pmdata(folder: Path):
    """Best-effort loader for a real PMData participant folder (pXX/fitbit/*.json)."""
    fit = folder / "fitbit"

    def rd(name):
        p = fit / name
        return json.loads(p.read_text()) if p.exists() else []

    steps, cals, sleep, rhr = defaultdict(float), defaultdict(float), defaultdict(float), {}
    for e in rd("steps.json"):
        d = _day(e.get("dateTime"))
        if d and _num(e.get("value")) is not None:
            steps[d] += _num(e["value"])
    for e in rd("calories.json"):
        d = _day(e.get("dateTime"))
        if d and _num(e.get("value")) is not None:
            cals[d] += _num(e["value"])
    for e in rd("sleep.json"):
        d = _day(e.get("dateOfSleep"))
        if d and _num(e.get("minutesAsleep")) is not None:
            sleep[d] += _num(e["minutesAsleep"]) / 60.0
    for e in rd("resting_heart_rate.json"):
        d, v = _day(e.get("dateTime")), e.get("value")
        v = _num(v.get("value")) if isinstance(v, dict) else _num(v)
        if d and v:
            rhr[d] = v
    days = sorted(set(steps) | set(sleep) | set(rhr))
    return [{"date": d, "steps": steps.get(d), "sleep_hours": sleep.get(d), "resting_hr": rhr.get(d),
             "calories": cals.get(d)} for d in days]


def _avg(rows, key):
    vals = [r[key] for r in rows if r.get(key) is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


class DataStore:
    def __init__(self, base=None):
        self.base = Path(base) if base else config.DATA_DIR
        self._cache = {}

    def rows(self, user_key):
        if user_key not in self._cache:
            real = self.base / "pmdata" / user_key
            syn = self.base / "synthetic" / user_key / "daily.csv"
            if (real / "fitbit").exists():
                self._cache[user_key] = _load_pmdata(real)
            elif syn.exists():
                self._cache[user_key] = _load_csv(syn)
            else:
                raise FileNotFoundError(f"No data for {user_key}. Run: python generate_data.py")
        return self._cache[user_key]

    def date_for_session(self, user_key, session_no):
        """Session N 'happens' at the end of week N of the data (clamped to the last day)."""
        rows = self.rows(user_key)
        d = rows[0]["date"] + dt.timedelta(days=7 * session_no - 1)
        return min(d, rows[-1]["date"])

    def summary(self, user_key, end_date, days=7):
        rows = self.rows(user_key)
        win = [r for r in rows if end_date - dt.timedelta(days=days) < r["date"] <= end_date]
        prev = [r for r in rows if end_date - dt.timedelta(days=2 * days) < r["date"] <= end_date - dt.timedelta(days=days)]
        cur = {m: _avg(win, m) for m in METRICS}
        out = {"as_of": str(end_date), "window_days": days, "days_with_data": len(win), "current": cur,
               "previous_week": {m: _avg(prev, m) for m in METRICS} if prev else None,
               "targets": TARGETS,
               "gap_to_target_pct": {m: round(gap_pct(m, cur[m]), 1) for m in TARGETS if cur[m] is not None}}
        return out

    def series(self, user_key, end_date=None):
        rows = self.rows(user_key)
        return [r for r in rows if end_date is None or r["date"] <= end_date]
