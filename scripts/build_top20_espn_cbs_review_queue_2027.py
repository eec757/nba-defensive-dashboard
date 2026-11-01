"""Prepare explicit ESPN/CBS source-review links for each top-20 NBA candidate.

This report intentionally does not claim that search results are actual player
profiles. It gives a reproducible human review queue and leaves all approvals
pending. No production edits.
"""
import json
import urllib.parse
from pathlib import Path

ROOT=Path("reports")
SOURCE=ROOT/"2027_top20_identity_source_exceptions.json"
OUT=ROOT/"2027_top20_espn_cbs_manual_profile_review.json"

def search_url(domain,name):
    return "https://www.google.com/search?"+urllib.parse.urlencode({"q":"site:"+domain+" "+name+" NBA player"})

def main():
    source=json.loads(SOURCE.read_text(encoding="utf-8"))
    rows=[]
    for player in source["players"]:
        name=player.get("nba_api_name")
        rows.append({"nba_player_id":player["nba_player_id"],
            "nba_api_name":name,
            "candidate_bref_ids":[c["bref_id"] for c in player["bref_candidates"]],
            "candidate_bref_urls":[c.get("url") for c in player["bref_candidates"]],
            "espn_review_search":search_url("espn.com/nba/player",name) if name else None,
            "cbs_review_search":search_url("cbssports.com/nba/players",name) if name else None,
            "espn_actual_profile_url":None,"cbs_actual_profile_url":None,
            "espn_profile_identity_checked":False,"cbs_profile_identity_checked":False,
            "nba_bref_dual_id_evidence_url":None,
            "exact_2026_27_position_evidence_url":None,
            "review_status":"manual_profile_review_required","approved":False})
    report={"players_checked":len(rows),"actual_espn_profiles_verified":0,
        "actual_cbs_profiles_verified":0,"independent_crosswalks_verified":0,
        "new_approvals":0,"published":False,"production_modified":False,
        "note":"Search URLs are navigation aids, not profile URLs or identity evidence. Reviewers must record actual source URLs and exact observed IDs/season positions.",
        "players":rows}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_ESPN_CBS_PROFILE_REVIEW_QUEUE",json.dumps({
        "players":len(rows),"actual_profiles_verified":0,
        "new_approvals":0,"published":False}))

if __name__=="__main__":main()
