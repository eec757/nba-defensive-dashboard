"""Generate an unapproved leaguewide identity-review queue from roster candidates."""
import csv
import json
from collections import defaultdict
from pathlib import Path

CANDIDATES = Path("reports/player_matching_2027.csv")
APPROVALS = Path("data/verified_player_ids_2027.csv")
OUTPUT = Path("reports/identity_review_queue_2027.csv")
FIELDS = ["priority", "team", "roster_name", "nba_player_id", "bref_id", "position",
          "regular_season_games", "review_status", "identity_evidence_status",
          "nba_profile_url", "bref_profile_url", "season_position_source"]

def main():
    with CANDIDATES.open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle))
    with APPROVALS.open(newline="", encoding="utf-8") as handle:
        approved = list(csv.DictReader(handle))
    by_pair = {(r["nba_player_id"], r["bref_id"]): r for r in approved}
    grouped = defaultdict(lambda: {"games_by_team": {}, "rows": []})
    for row in candidates:
        if row["status"] != "single_name_candidate" or not row["nba_player_id"] or not row["bref_id"]:
            continue
        key = (row["nba_player_id"], row["bref_id"])
        grouped[key]["rows"].append(row)
        team = row["team"]
        grouped[key]["games_by_team"][team] = max(
            grouped[key]["games_by_team"].get(team, 0), int(row["regular_season_games"] or 0)
        )
    queue = []
    for key, group in grouped.items():
        rows = sorted(group["rows"], key=lambda r: (-int(r["regular_season_games"] or 0), r["team"]))
        row = rows[0]
        previous = by_pair.get(key)
        if previous and previous["verified"].strip().lower() == "true":
            continue
        games = sum(group["games_by_team"].values())
        queue.append({
            "priority": 0, "team": ";".join(sorted(group["games_by_team"])),
            "roster_name": row["roster_name"], "nba_player_id": key[0], "bref_id": key[1],
            "position": row["position"], "regular_season_games": games,
            "review_status": "staged_unapproved" if previous else "candidate_unapproved",
            "identity_evidence_status": "requires_independent_exact_id_verification",
            "nba_profile_url": f"https://www.nba.com/player/{key[0]}",
            "bref_profile_url": f"https://www.basketball-reference.com/players/{key[1][0]}/{key[1]}.html",
            "season_position_source": f"https://www.basketball-reference.com/teams/{row['team']}/2027.html",
        })
    queue.sort(key=lambda r: (-r["regular_season_games"], r["team"], r["roster_name"], r["nba_player_id"]))
    for i, row in enumerate(queue, 1):
        row["priority"] = i
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(queue)
    print("IDENTITY_REVIEW_QUEUE", json.dumps({
        "unapproved_candidates": len(queue),
        "candidate_player_game_rows": sum(r["regular_season_games"] for r in queue),
        "top_10": [{"name": r["roster_name"], "team": r["team"], "games": r["regular_season_games"]} for r in queue[:10]],
        "output": str(OUTPUT), "auto_approved": 0,
        "warning": "Name/team matching is NOT independent identity verification; profile URLs are review aids, not evidence of exact ID matching."
    }))

if __name__ == "__main__":
    main()
