"""Generate an evidence review packet for seven unapproved, non-excluded candidates.

Source candidates are produced by the combined read-only audit. No approvals are granted.
"""
import csv
import json
from pathlib import Path
from display_exclusions_2027 import EXCLUDED_PLAYER_IDS

KNOWN={
 "1626171":("Bobby Portis","portibo01","MIA","Q19667582"),
 "1641713":("GG Jackson","jacksgg01","MEM","Q115492105"),
 "1641842":("Ron Holland","hollaro01","DET","Q116407941"),
 "1643515":("Christian Anderson","anderch02","CHO","Q133691210"),
 "1629057":("Robert Williams III","williro04","POR","Q28151848"),
 "1642383":("Walter Clayton Jr.","claytwa01","DAL","Q117262884"),
 "1641747":("DaRon Holmes II","holmeda01","DEN","Q115492041"),
}

def main():
    with Path("reports/2027_supported_identity_review_queue.csv").open(newline="",encoding="utf-8") as f:
        queue=list(csv.DictReader(f))
    ids={r["nba_player_id"] for r in queue}
    if ids != set(KNOWN) or ids & EXCLUDED_PLAYER_IDS or len(queue)!=len(ids):
        raise ValueError("Candidate set changed; independently review and update packet before continuing")
    fields=["nba_player_id","player","bref_id","candidate_position","game_rows","defending_teams","wikidata_identity_url","season_roster_url","identity_evidence_checked","position_evidence_checked","human_approval","review_notes"]
    out=Path("reports/2027_seven_player_approval_review_packet.csv")
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in queue:
            pid=r["nba_player_id"];name,bref,team,q=KNOWN[pid]
            w.writerow({"nba_player_id":pid,"player":name,"bref_id":bref,"candidate_position":r["candidate_position"],"game_rows":r["game_rows"],"defending_teams":r["defending_teams"],"wikidata_identity_url":f"https://www.wikidata.org/wiki/{q}","season_roster_url":f"https://www.basketball-reference.com/teams/{team}/2027.html","identity_evidence_checked":"pending","position_evidence_checked":"pending","human_approval":"pending","review_notes":""})
    print("SEVEN_PLAYER_REVIEW_PACKET",json.dumps({"players":len(queue),"game_rows":sum(int(r["game_rows"]) for r in queue),"approvals":0,"excluded_players_omitted":True}))

if __name__=="__main__":main()
