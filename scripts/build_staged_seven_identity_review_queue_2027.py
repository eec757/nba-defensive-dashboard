"""Rank unverified NBA IDs by actual unmatched player-game rows and affected teams.

Only produces an evidence-review queue. Never assumes identity, position, or
publication eligibility. Requires the staged unmatched-row report.
"""
import json
from collections import defaultdict
from pathlib import Path

SOURCE=Path("reports/2027_staged_seven_player_unmatched_game_rows_by_team.json")
OUT=Path("reports/2027_staged_seven_player_identity_review_priority_queue.json")

def main():
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    players=defaultdict(lambda:{"unmatched_game_rows":0,"affected_teams":set(),
                                 "game_ids":set(),"blocked_position_cells_in_affected_teams":0})
    for team in data["teams"]:
        for item in team["unmatched_player_ids"]:
            p=players[str(item["nba_player_id"])]
            p["unmatched_game_rows"]+=item["unverified_game_rows"]
            p["affected_teams"].add(team["team"])
            p["game_ids"].update(item["game_ids"])
            p["blocked_position_cells_in_affected_teams"]+=team["blocked_position_cells"]
    rows=[{"nba_player_id":pid,"unmatched_game_rows":v["unmatched_game_rows"],
           "affected_teams":sorted(v["affected_teams"]),
           "affected_team_count":len(v["affected_teams"]),
           "blocked_position_cells_in_affected_teams":v["blocked_position_cells_in_affected_teams"],
           "game_ids":sorted(v["game_ids"]),
           "identity_verified":False,"exact_position_verified":False,
           "review_status":"independent evidence required"}
          for pid,v in players.items()]
    rows.sort(key=lambda r:(-r["unmatched_game_rows"],
        -r["blocked_position_cells_in_affected_teams"],r["nba_player_id"]))
    if sum(r["unmatched_game_rows"] for r in rows)!=data["unmatched_rows"]:
        raise ValueError("Priority queue does not reconcile to unmatched rows")
    report={"source":"staged seven-player unmatched-game report",
        "unmatched_rows":data["unmatched_rows"],"unmatched_player_count":len(rows),
        "priority_players":rows,"crosswalk_modified":False,"publication_ready":False,
        "note":"Rank reflects unmatched rows and affected coverage cells, not identity evidence. No automatic approval."}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("STAGED_SEVEN_IDENTITY_REVIEW_QUEUE",json.dumps({
        "unmatched_players":len(rows),"unmatched_rows":data["unmatched_rows"],
        "top_player_ids":[r["nba_player_id"] for r in rows[:10]],"published":False}))

if __name__=="__main__":main()
