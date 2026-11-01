"""Read-only provenance report for unresolved 2026-27 position classifications.

These are documented source observations, not fresh HTTP fetches. Do not
promote any candidate to an exact five-position role based on this report.
"""
import json
from datetime import date
from pathlib import Path
from classify_roster_position_2027 import classify_roster_position

OBSERVATIONS=[
 {"nba_id":"1643633","player":"Graham Ike","bref_id":"ikegr01","candidate":"PF","rows":4,"observations":[
  {"url":"https://www.basketball-reference.com/teams/GSW/2027.html","label":"F","source":"Basketball Reference 2026-27 team roster"},
  {"url":"https://www.nba.com/player/1643633","label":"Forward-Center","source":"NBA player profile"}]},
 {"nba_id":"1643568","player":"Nick Martinelli","bref_id":"martini01","candidate":"SF","rows":1,"observations":[
  {"url":"https://www.basketball-reference.com/teams/LAC/2027.html","label":"F","source":"Basketball Reference 2026-27 team roster"},
  {"url":"https://www.nba.com/player/1643568","label":"Forward","source":"NBA player profile"}]},
 {"nba_id":"1643813","player":"Alpha Diallo","bref_id":"diallal01","candidate":"SG","rows":1,"observations":[
  {"url":"https://www.basketball-reference.com/teams/DEN/2027.html","label":"G","source":"Basketball Reference 2026-27 team roster"},
  {"url":"https://www.nba.com/player/1643813","label":"Guard","source":"NBA player profile"}]},
]

def main():
    rows=[]
    for p in OBSERVATIONS:
        classified=[{**o,"classification":classify_roster_position(o["label"]),
                     "retrieval_date":None,"retrieval_status":"not_refetched_in_this_run"}
                    for o in p["observations"]]
        rows.append({"nba_id":p["nba_id"],"player":p["player"],"candidate_bref_id":p["bref_id"],
                     "candidate_position":p["candidate"],"excluded_game_rows":p["rows"],
                     "source_observations":classified,"exact_position_supported":False,
                     "identity_link_verified":False if p["nba_id"]=="1643813" else None,
                     "approved":False})
    out=Path("reports/2027_three_player_position_source_provenance.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"scope":"historical documented observations; not a live fetch",
        "generated_date":date.today().isoformat(),"players":rows,
        "excluded_game_rows":sum(p["rows"] for p in OBSERVATIONS),
        "crosswalk_modified":False,"publication_ready":False},indent=2)+"\n",encoding="utf-8")
    print("THREE_PLAYER_POSITION_PROVENANCE",json.dumps({"players":len(rows),"excluded_game_rows":6,"all_unresolved":True,"publication_ready":False}))

if __name__=="__main__":main()
