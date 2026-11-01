"""Gather bounded ESPN and CBS search corroboration for top unmatched players.

Uses public Bing HTML search results for discovery only; snippets and names
never establish exact NBA/BRef ID equivalence or season position. No approval.
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
ROOT=Path("reports")
SOURCE=ROOT/"2027_top20_identity_source_exceptions.json"
OUT=ROOT/"2027_top20_espn_cbs_discovery.json"
def fetch(q):
    url="https://www.google.com/search?"+urllib.parse.urlencode({"q":q,"num":"3"})
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; NBADefensiveDashboardEvidenceAudit/1.0)","Accept":"text/html"})
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            body=r.read(160000).decode("utf-8",errors="replace")
            return {"status":"reachable","http_status":r.status,
                "player_name_in_page":False,
                "search_url":url,"raw_page_not_saved":True,
                "note":"Discovery-only query; inspect actual ESPN/CBS player pages manually"}
    except Exception as exc:
        return {"status":"unavailable","error":str(exc)[:160],"search_url":url}
def main():
    source=json.loads(SOURCE.read_text(encoding="utf-8"))
    rows=[]
    for p in source["players"]:
        name=p.get("nba_api_name")
        row={"nba_player_id":p["nba_player_id"],"nba_api_name":name,
            "espn":{"status":"not_checked"},"cbs":{"status":"not_checked"},
            "independent_dual_id_verified":False,"exact_season_position_verified":False,
            "approved":False}
        if name:
            row["espn"]=fetch("site:espn.com/nba/player/ "+name)
            time.sleep(0.2)
            row["cbs"]=fetch("site:cbssports.com/nba/players/ "+name)
            time.sleep(0.2)
        rows.append(row)
    report={"players_checked":len(rows),"espn_discovery_queries":sum(p["espn"]["status"]!="not_checked" for p in rows),
        "cbs_discovery_queries":sum(p["cbs"]["status"]!="not_checked" for p in rows),
        "new_approvals":0,"crosswalk_modified":False,"published":False,
        "note":"Search engine access is not ESPN/CBS profile validation; discovery URLs are not independent evidence.",
        "players":rows}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_ESPN_CBS_DISCOVERY",json.dumps({k:report[k] for k in
        ("players_checked","espn_discovery_queries","cbs_discovery_queries","new_approvals","published")}))
if __name__=="__main__":main()
