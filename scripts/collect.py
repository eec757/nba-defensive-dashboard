"""Build season-separated team scoring summaries from downloadable NBA-derived CSVs.

Source: BoxScore Lab (CC BY 4.0), https://boxscorelab.com/downloads/
No guessed values: unexpected schemas fail safely without changing existing data.
"""
import csv
import io
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

SEASONS = ("2025-26", "2026-27")
OUTPUT = Path("data/summary.json")
BASE_URL = "https://boxscorelab.com/downloads"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "nba-defensive-dashboard/1.0 (CSV data update)"})


def download(season):
    url = f"{BASE_URL}/{season}-team-game-results.csv"
    for attempt in range(1, 4):
        try:
            response = SESSION.get(url, timeout=25)
            response.raise_for_status()
            reader = csv.DictReader(io.StringIO(response.text.lstrip("\ufeff")))
            if not reader.fieldnames:
                raise ValueError("CSV missing headers")
            rows = list(reader)
            print(f"{season}: downloaded {len(rows)} rows; fields: {reader.fieldnames}", flush=True)
            return rows
        except (requests.RequestException, ValueError) as exc:
            print(f"{season}: CSV attempt {attempt}/3 failed: {exc}", file=sys.stderr, flush=True)
            if attempt == 3:
                raise RuntimeError(f"Unable to download {season} from {url}; existing data preserved") from exc
            time.sleep(attempt * 3)


def normalized(row):
    return {str(k).strip().lower().replace("-", "_").replace(" ", "_"): v for k, v in row.items() if k is not None}


def pick(row, *names):
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip() != "":
            return value
    return None


def number(value):
    return float(str(value).replace(",", ""))


def summarize(raw_rows, season):
    rows = [normalized(row) for row in raw_rows]
    if not rows:
        return {"games": 0, "teams": []}

    totals = defaultdict(lambda: {"team": "", "gp": 0, "pts": 0.0, "allowed": 0.0})
    for row in rows:
        team = pick(row, "team", "team_abbreviation", "team_abbr")
        pts = pick(row, "points", "pts", "team_points")
        allowed = pick(row, "opponent_points", "opp_pts", "points_allowed")
        if team is None or pts is None or allowed is None:
            raise ValueError(f"{season}: missing team/points/opponent_points. Fields: {list(row)}")
        item = totals[str(team)]
        item["team"] = str(team)
        item["gp"] += 1
        item["pts"] += number(pts)
        item["allowed"] += number(allowed)

    teams = []
    for item in totals.values():
        gp = item["gp"]
        teams.append({
            "team": item["team"],
            "gp": gp,
            "ppg": round(item["pts"] / gp, 2),
            "opp_ppg": round(item["allowed"] / gp, 2),
            "quality": "Calculated/Derived from BoxScore Lab NBA-derived game results",
        })
    for field, metric, reverse in (
        ("scoring_rank", "ppg", True),
        ("defense_rank", "opp_ppg", False),
    ):
        ordered = sorted(teams, key=lambda t: (-t[metric] if reverse else t[metric], t["team"]))
        for rank, item in enumerate(ordered, 1):
            item[field] = rank
    return {"games": len(rows) // 2, "teams": sorted(teams, key=lambda t: t["team"])}

def main():
    seasons = {season: summarize(download(season), season) for season in SEASONS}
    if not seasons["2025-26"]["teams"]:
        raise RuntimeError("Historical season has no teams; refusing to replace existing snapshot")
    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "BoxScore Lab, https://boxscorelab.com/downloads/ (CC BY 4.0; NBA-derived)",
        "seasons": seasons,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUTPUT)
    print(f"Wrote {OUTPUT}", flush=True)


if __name__ == "__main__":
    main()
