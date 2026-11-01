"""Probe verification-source availability for top unmatched NBA IDs.

Diagnostics only. No scraping, identity approval, crosswalk changes, or publication.
Requests are bounded and source failures are recorded rather than assumed valid.
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path("reports")
QUEUE=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
OUT=ROOT/"2027_verification_source_health.json"
SOURCES={
    "nba_players":{"url":"https://www.nba.com/players","role":"official_identity","season_position_verified":False},
    "nba_stats":{"url":"https://www.nba.com/stats/overview","role":"official_stats","season_position_verified":False},
    "basketball_reference":{"url":"https://www.basketball-reference.com/","role":"bref_identity_and_season_roster","season_position_verified":False},
    "espn":{"url":"https://www.espn.com/nba/players","role":"independent_position_crosscheck","season_position_verified":False},
    "cbs":{"url":"https://www.cbssports.com/nba/stats/","role":"independent_position_crosscheck","season_position_verified":False},
    "nba_api_repository":{"url":"https://github.com/swar/nba_api","role":"nba_api_library_documentation","season_position_verified":False},
}
def probe(url):
    request=urllib.request.Request(url,headers={"User-Agent":"nba-defensive-dashboard-source-health/1.0 (public availability check)","Accept":"text/html"})
    try:
        with urllib.request.urlopen(request,timeout=8) as response:
            return {"status":"reachable","http_status":response.status,"final_url":response.geturl()}
    except urllib.error.HTTPError as exc:
        return {"status":"http_error","http_status":exc.code,"error":str(exc)[:200]}
    except Exception as exc:
        return {"status":"unavailable","error":str(exc)[:200]}

def main():
    priority=json.loads(QUEUE.read_text(encoding="utf-8"))["priority_players"][:20]
    results={key:{**info,**probe(info["url"])} for key,info in SOURCES.items()}
    report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
        "scope":"top 20 unmatched NBA IDs","priority_nba_ids":[p["nba_player_id"] for p in priority],
        "source_health":results,"identity_matches_verified":0,
        "positions_verified":0,"players_approved":0,
        "publication_ready":False,"production_modified":False,
        "note":"HTTP reachability is not evidence of player identity or exact 2026-27 position. Endpoint access may vary by environment; manual source review remains required."}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("VERIFICATION_SOURCE_HEALTH",json.dumps({"reachable":[k for k,v in results.items() if v["status"]=="reachable"],
        "blocked_or_unavailable":[k for k,v in results.items() if v["status"]!="reachable"],
        "priority_players":len(priority),"approvals":0,"published":False}))

if __name__=="__main__":main()
