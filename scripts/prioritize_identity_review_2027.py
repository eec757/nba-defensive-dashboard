"""Prioritize unmatched 2027 player-game IDs for human review; never approve."""
import csv
import json
from pathlib import Path

FAILED_TEAMS = {"MIA", "OKC", "PHO", "SAC"}
source = json.loads(Path("reports/unmatched_player_games_2027.json").read_text())
rows = []
for player in source["players"]:
    affected = sorted(FAILED_TEAMS.intersection(player["defending_teams"]))
    rows.append({
        "nba_player_id": player["nba_player_id"],
        "unmatched_game_rows": player["game_rows"],
        "priority": "team_gate" if affected else "other",
        "affected_failed_teams": ",".join(affected),
        "defending_teams": json.dumps(player["defending_teams"], sort_keys=True),
        "game_ids": ",".join(player["game_ids"]),
        "review_candidates": json.dumps(player["review_queue_matches"], sort_keys=True),
        "status": "requires_independent_review",
    })
rows.sort(key=lambda x: (x["priority"] != "team_gate", -x["unmatched_game_rows"], x["nba_player_id"]))
assert len(rows) == source["unmatched_player_ids"]
assert sum(r["unmatched_game_rows"] for r in rows) == source["unmatched_game_rows"]
out = Path("reports/prioritized_identity_review_2027.csv")
with out.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print("REVIEW_QUEUE", json.dumps({"ids":len(rows),"rows":source["unmatched_game_rows"],"priority_ids":sum(r["priority"]=="team_gate" for r in rows),"publication_ready":False}))

print("PRIORITY_ONE_IDENTITIES", json.dumps([{"nba_player_id":r["nba_player_id"],"unmatched_game_rows":r["unmatched_game_rows"],"failed_teams":r["affected_failed_teams"],"game_ids":r["game_ids"]} for r in rows if r["priority"] == "team_gate"]))
