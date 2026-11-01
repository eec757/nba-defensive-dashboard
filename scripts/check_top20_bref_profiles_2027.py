"""Read-only candidate Basketball Reference profile and independent-source checks.

Checks public profile metadata and NBA static names for top 20 unmatched IDs.
Name agreement is corroboration, NEVER proof of NBA↔BRef ID linkage.
No crosswalk changes, approvals, or publication.
"""
import csv
import html
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from nba_api.stats.static import players

ROOT=Path("reports")
QUEUE=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
CANDIDATES=ROOT/"proposed_verified_player_ids_2027.csv"
OUT=ROOT/"2027_top20_direct_profile_review.json"
USER_AGENT="NBA-Defensive-Dashboard/1.0 (public player identity research)"
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"text/html"})
    try:
        with urllib.request.urlopen(req,timeout=12) as resp:
            raw=resp.read(400000).decode("utf-8",errors="replace")
            title=re.search(r"<title[^>]*>(.*?)</title>",raw,re.I|re.S)
            heading=re.search(r"<h1[^>]*>(.*?)</h1>",raw,re.I|re.S)
            clean=lambda s:html.unescape(re.sub(r"<[^>]+>"," ",s)).strip() if s else None
            return {"status":"reachable","http_status":resp.status,"title":clean(title.group(1)) if title else None,
                "heading":clean(heading.group(1)) if heading else None}
    except urllib.error.HTTPError as exc:
        return {"status":"http_error","http_status":exc.code}
    except Exception as exc:return {"status":"unavailable","error":str(exc)[:180]}
def main():
    queue=json.loads(QUEUE.read_text(encoding="utf-8"))["priority_players"][:20]
    with CANDIDATES.open(newline="",encoding="utf-8") as f: proposed=list(csv.DictReader(f))
    by_id={}
    for row in proposed:by_id.setdefault(str(row.get("nba_player_id","")),set()).add(str(row.get("bref_id","")))
    results=[]
    for item in queue:
        pid=str(item["nba_player_id"])
        nba=players.find_player_by_id(int(pid))
        refs=[]
        for bref in sorted(by_id.get(pid,set())-{""}):
            # BRef player URL derives from candidate ID; never treat as confirmed.
            if not re.fullmatch(r"[a-z0-9]{4,20}",bref):
                refs.append({"candidate_bref_id":bref,"status":"invalid_candidate_id"});continue
            url="https://www.basketball-reference.com/players/"+bref[0]+"/"+bref+".html"
            refs.append({"candidate_bref_id":bref,"url":url,**get(url)})
            time.sleep(0.7)
        results.append({"nba_player_id":pid,"nba_api_name":nba["full_name"] if nba else None,
            "basketball_reference_candidates":refs,
            "crosswalk_independently_verified":False,
            "exact_2026_27_position_verified":False,
            "approved":False,
            "review_status":"requires_independent_exact_dual_id_evidence"})
    report={"players_checked":len(results),
        "candidate_profiles_reachable":sum(r["status"]=="reachable" for p in results for r in p["basketball_reference_candidates"]),
        "candidate_profiles_blocked_or_missing":sum(r["status"]!="reachable" for p in results for r in p["basketball_reference_candidates"]),
        "new_independent_crosswalk_approvals":0,"production_modified":False,"published":False,
        "note":"Page existence, headings and matching names are NOT independent NBA/BRef dual-ID evidence. ESPN/CBS are secondary cross-checks; no scraping or automatic approvals.",
        "players":results}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_BREF_PROFILE_REVIEW",json.dumps({k:report[k] for k in
        ("players_checked","candidate_profiles_reachable","candidate_profiles_blocked_or_missing","new_independent_crosswalk_approvals","published")}))
if __name__=="__main__":main()
