"""Read-only report of broad/ambiguous roster classifications for excluded players."""
import json
from pathlib import Path
from classify_roster_position_2027 import classify_roster_position

OUT=Path("reports/2027_three_player_position_ambiguity.json")
SOURCES=[
    {"nba_player_id":"1643633","name":"Graham Ike","season_roster_label":"F","other_reported_label":"F-C","candidate_position":"PF","game_rows":4},
    {"nba_player_id":"1643568","name":"Nick Martinelli","season_roster_label":"F","other_reported_label":"F","candidate_position":"SF","game_rows":1},
    {"nba_player_id":"1643813","name":"Alpha Diallo","season_roster_label":"G","other_reported_label":"SF","candidate_position":"SG","game_rows":1},
]

def main():
    rows=[]
    for p in SOURCES:
        roster=classify_roster_position(p["season_roster_label"])
        other=classify_roster_position(p["other_reported_label"])
        if roster["status"]!="ambiguous":raise ValueError("Expected unresolved broad season-roster label")
        rows.append({**p,"roster_classification":roster,"other_classification":other,
                     "approved_position":None,"position_resolved":False,
                     "independent_exact_identity_link_pending":p["nba_player_id"]=="1643813"})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({"source":"documented research exception labels; not a live source refresh",
        "players":rows,"excluded_game_rows":sum(x["game_rows"] for x in rows),
        "publication_ready":False,"crosswalk_modified":False},indent=2)+"\n",encoding="utf-8")
    print("THREE_PLAYER_POSITION_AMBIGUITY",json.dumps({"players":3,"ambiguous":3,"excluded_game_rows":6,"publication_ready":False}))

if __name__=="__main__":main()
