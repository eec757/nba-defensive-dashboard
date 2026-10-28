"""Evidence readiness for the three unresolved 2026–27 players.

Read-only. Historical source observations are not live verification or approval.
"""
import json
from pathlib import Path
from report_three_player_position_source_provenance_2027 import OBSERVATIONS
from classify_roster_position_2027 import classify_roster_position

OUT=Path("reports/2027_three_player_independent_verification_readiness.json")
def build():
    players=[]
    for p in OBSERVATIONS:
        exact=[o for o in p["observations"] if classify_roster_position(o["label"])["status"]=="exact"]
        identity_verified=False  # No independently corroborated identity decision in this report
        position_verified=False  # No exact season-specific evidence and human review in this report
        players.append({"nba_player_id":p["nba_id"],"player":p["player"],"candidate_bref_id":p["bref_id"],
            "candidate_position":p["candidate"],"raw_game_rows_retained":p["rows"],
            "identity_verified":identity_verified,"exact_position_verified":position_verified,
            "identity_only_team_metrics_eligible":identity_verified,
            "exact_position_metrics_eligible":identity_verified and position_verified,
            "historical_source_observations":[{"url":o["url"],"label":o["label"],
                 "classification":classify_roster_position(o["label"]),
                 "retrieval_date":None,"verified_live":False} for o in p["observations"]],
            "historical_exact_position_observation_count":len(exact),
            "next_evidence_required":(["independent exact NBA-to-BRef identity corroboration"] if p["nba_id"]=="1643813" else [])+
                ["2026-27 exact PG/SG/SF/PF/C evidence with retrieval date and human approval"],
            "review_status":"pending"})
    return {"players":players,"raw_game_rows_retained":sum(p["raw_game_rows_retained"] for p in players),
            "identity_only_promotions":0,"exact_position_promotions":0,
            "published":False,"crosswalk_modified":False}
def main():
    report=build()
    assert len(report["players"])==3 and report["raw_game_rows_retained"]==6
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("THREE_PLAYER_VERIFICATION_READINESS",json.dumps({"players":3,"pending":3,
        "raw_game_rows_retained":6,"identity_only_promotions":0,"exact_position_promotions":0,
        "published":False}))
if __name__=="__main__":main()
