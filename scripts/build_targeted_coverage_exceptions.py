"""Build a read-only prioritized exception report from existing audit outputs.

Run after audit_proposed_game_coverage.py and audit_unmatched_player_games.py.
Never approves identities or publishes defensive data.
"""
import csv
import json
from pathlib import Path

REPORTS = Path("reports")
PRIORITY = {"MIA", "OKC", "PHO", "SAC"}

def main():
    coverage = json.loads((REPORTS / "proposed_game_coverage_2027.json").read_text())
    unmatched = json.loads((REPORTS / "unmatched_player_games_2027.json").read_text())
    teams = coverage["teams"]
    failures = []
    for team, info in teams.items():
        bad_positions = [pos for pos, detail in info["positions"].items()
                         if not detail["passes_95_pct"]]
        if not info["passes_95_pct"] or bad_positions:
            failures.append({"team": team, "priority": team in PRIORITY,
                             "coverage_pct": info["coverage_pct"],
                             "unknown_rows": info["unknown_rows"],
                             "failed_positions": bad_positions})
    failures.sort(key=lambda x: (not x["priority"], x["coverage_pct"], x["team"]))
    affected = {f["team"] for f in failures}
    candidates = []
    for p in unmatched["players"]:
        hits = {t: n for t, n in p["defending_teams"].items() if t in affected}
        if hits:
            candidates.append({"nba_player_id": p["nba_player_id"],
                               "unmatched_game_rows": p["game_rows"],
                               "affected_team_rows": sum(hits.values()),
                               "defending_teams": hits,
                               "game_ids": p["game_ids"],
                               "review_queue_matches": p["review_queue_matches"]})
    candidates.sort(key=lambda x: (-x["affected_team_rows"], x["nba_player_id"]))
    result = {"coverage_failures": failures, "unmatched_candidates": candidates,
              "publication_ready": False,
              "note": "Investigation only; no inferred identities or approval."}
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "targeted_coverage_exceptions_2027.json").write_text(json.dumps(result, indent=2) + "\n")
    with (REPORTS / "targeted_coverage_exceptions_2027.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nba_player_id", "affected_team_rows", "unmatched_game_rows",
                    "defending_team_counts", "game_ids", "review_queue_matches"])
        for p in candidates:
            w.writerow([p["nba_player_id"], p["affected_team_rows"],
                        p["unmatched_game_rows"], json.dumps(p["defending_teams"], sort_keys=True),
                        ";".join(p["game_ids"]), json.dumps(p["review_queue_matches"])])
    print(f"Coverage failures: {len(failures)}; unmatched candidates: {len(candidates)}")

if __name__ == "__main__":
    main()
