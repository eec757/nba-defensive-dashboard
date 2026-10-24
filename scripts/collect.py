"""Collect NBA team scoring metrics from official NBA game logs.

A failed or incomplete fetch never overwrites the last successful snapshot.
"""
import json
import random
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from nba_api.stats.endpoints import leaguegamelog
from requests.exceptions import RequestException

SEASONS = ("2025-26", "2026-27")
OUTPUT = Path("data/summary.json")
ATTEMPTS = 3
TIMEOUT_SECONDS = 35


def fetch_rows(season):
    for attempt in range(1, ATTEMPTS + 1):
        try:
            print(f"Fetching {season} team game logs (attempt {attempt}/{ATTEMPTS})", flush=True)
            response = leaguegamelog.LeagueGameLog(
                season=season,
                season_type_all_star="Regular Season",
                player_or_team_abbreviation="T",
                timeout=TIMEOUT_SECONDS,
            )
            rows = response.get_normalized_dict().get("LeagueGameLog")
            if not isinstance(rows, list):
                raise ValueError(f"Unexpected NBA API response for {season}")
            return rows
        except (RequestException, ValueError, KeyError) as exc:
            print(f"NBA API request failed for {season}: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            if attempt == ATTEMPTS:
                raise RuntimeError(
                    f"NBA.com could not provide {season} game logs after {ATTEMPTS} attempts. "
                    "This may be an NBA.com timeout or GitHub-hosted runner access restriction. "
                    "Existing data has not been modified."
                ) from exc
            time.sleep(3 * attempt + random.uniform(0, 2))


def summarize(rows):
    games = defaultdict(list)
    for row in rows:
        if row.get("GAME_ID") and row.get("TEAM_ID"):
            games[str(row["GAME_ID"])].append(row)

    totals = defaultdict(lambda: {"team": "", "gp": 0, "pts": 0, "allowed": 0})
    completed = 0
    for sides in games.values():
        if len(sides) != 2 or sides[0]["TEAM_ID"] == sides[1]["TEAM_ID"]:
            continue
        if any(side.get("PTS") is None for side in sides):
            continue
        completed += 1
        a, b = sides
        for team, opponent in ((a, b), (b, a)):
            t = totals[str(team["TEAM_ID"])]
            t["team"] = team["TEAM_ABBREVIATION"]
            t["gp"] += 1
            t["pts"] += int(team["PTS"])
            t["allowed"] += int(opponent["PTS"])

    teams = []
    for t in totals.values():
        if t["gp"]:
            teams.append({
                "team": t["team"],
                "gp": t["gp"],
                "ppg": round(t["pts"] / t["gp"], 2),
                "opp_ppg": round(t["allowed"] / t["gp"], 2),
                "quality": "Derived from NBA official game logs",
            })
    for field, metric, descending in (
        ("scoring_rank", "ppg", True),
        ("defense_rank", "opp_ppg", False),
    ):
        ordered = sorted(teams, key=lambda t: (-t[metric] if descending else t[metric], t["team"]))
        for rank, team in enumerate(ordered, 1):
            team[field] = rank
    return {"games": completed, "teams": sorted(teams, key=lambda t: t["team"])}


def main():
    # Fetch both seasons before writing anything: no partial snapshots.
    seasons = {season: summarize(fetch_rows(season)) for season in SEASONS}
    if not seasons["2025-26"]["teams"]:
        raise RuntimeError("NBA.com returned no completed 2025-26 games; refusing to overwrite existing data.")
    result = {"updated_at": datetime.now(timezone.utc).isoformat(), "seasons": seasons}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(f"Updated {OUTPUT} successfully", flush=True)


if __name__ == "__main__":
    main()
