"""Prepare evidence-required review packet for highest-impact unmatched IDs.

No player is approved or staged by this script.
"""
import csv
import json
from pathlib import Path

SOURCE=Path("reports/2027_staged_seven_player_identity_review_priority_queue.json")
OUT=Path("reports/2027_top_unmatched_player_independent_evidence_packet.csv")
FIELDS=["nba_player_id","unmatched_game_rows","affected_teams","affected_team_count",
"candidate_name","candidate_bref_id","independent_nba_id_evidence_url",
"independent_bref_id_evidence_url","exact_2026_27_position",
"season_position_evidence_url","reviewer","review_date",
"identity_review_status","position_review_status","promotion_approved"]

def main():
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    rows=[]
    for p in data["priority_players"][:20]:
        rows.append({"nba_player_id":p["nba_player_id"],
            "unmatched_game_rows":p["unmatched_game_rows"],
            "affected_teams":",".join(p["affected_teams"]),
            "affected_team_count":p["affected_team_count"],
            "candidate_name":"","candidate_bref_id":"",
            "independent_nba_id_evidence_url":"",
            "independent_bref_id_evidence_url":"",
            "exact_2026_27_position":"",
            "season_position_evidence_url":"",
            "reviewer":"","review_date":"",
            "identity_review_status":"pending_independent_evidence",
            "position_review_status":"pending_exact_season_evidence",
            "promotion_approved":"false"})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS)
        writer.writeheader();writer.writerows(rows)
    print("TOP_UNMATCHED_INDEPENDENT_EVIDENCE_PACKET",json.dumps({
        "players":len(rows),"game_rows_in_packet":sum(int(x["unmatched_game_rows"]) for x in rows),
        "approvals":0,"published":False}))

if __name__=="__main__":main()
