"""Produce a review-only queue for season-position-supported identities not in baseline.

This report is not an approval, and does not change verified player IDs.
"""
import csv
import json
from pathlib import Path
from display_exclusions_2027 import EXCLUDED_PLAYER_IDS


def main():
    missing=json.loads(Path("reports/missing_player_position_evidence_2027.json").read_text())
    unmatched=json.loads(Path("reports/unmatched_player_games_2027.json").read_text())
    with Path("reports/proposed_verified_player_ids_2027.csv").open(newline="",encoding="utf-8") as f:
        proposed=list(csv.DictReader(f))
    with Path("reports/season_position_evidence_2027.csv").open(newline="",encoding="utf-8") as f:
        season=list(csv.DictReader(f))
    supported={(r["nba_player_id"],r["bref_id"]) for r in season if r["status"]=="supported"}
    baseline={r["nba_player_id"] for r in proposed if (r["nba_player_id"],r["bref_id"]) in supported}
    missing_by_id={p["nba_player_id"]:p for p in missing["players"]}
    queue=[]
    for player in unmatched["players"]:
        pid=player["nba_player_id"]
        if pid in baseline or pid in EXCLUDED_PLAYER_IDS:
            continue
        candidate=missing_by_id.get(pid)
        if not candidate or not candidate["season_position_verified"]:
            continue
        positions={e["position"] for e in candidate["season_position_evidence"]}
        if len(positions)!=1:
            continue
        queue.append({"nba_player_id":pid,"candidate_position":next(iter(positions)),
                      "game_rows":player["game_rows"],"defending_teams":",".join(sorted(player["defending_teams"])),
                      "review_status":"pending_independent_identity_and_position_review",
                      "approval_status":"not_approved"})
    queue.sort(key=lambda x:(-int(x["game_rows"]),x["nba_player_id"]))
    out=Path("reports/2027_supported_identity_review_queue.csv")
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["nba_player_id","candidate_position","game_rows","defending_teams","review_status","approval_status"])
        w.writeheader();w.writerows(queue)
    print("SUPPORTED_IDENTITY_REVIEW_QUEUE",json.dumps({"players":len(queue),"game_rows":sum(int(x["game_rows"]) for x in queue),"excluded_ids_omitted":sorted(EXCLUDED_PLAYER_IDS),"approvals":0}))

if __name__=="__main__":main()
