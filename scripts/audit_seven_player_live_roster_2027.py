"""Read-only live 2026-27 roster-cell checks for seven pending players."""
import csv
import json
import time
from pathlib import Path
from urllib.parse import urlparse
import requests
from audit_season_position_evidence import roster_positions

SOURCE=Path("reports/2027_seven_player_unapproved_crosswalk_candidates.csv")
OUT=Path("reports/2027_seven_player_live_roster_positions.csv")

def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    if len(rows)!=7 or len({r["nba_player_id"] for r in rows})!=7:raise ValueError("Expected seven distinct pending players")
    cache={};results=[]
    with requests.Session() as session:
        session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; NBA research position audit)"})
        for row in rows:
            url=row["position_source"];parsed=urlparse(url)
            if parsed.scheme!="https" or parsed.hostname!="www.basketball-reference.com" or not parsed.path.startswith("/teams/") or not parsed.path.endswith("/2027.html"):
                status,observed,reason="unverified","","invalid_roster_source"
            else:
                if url not in cache:
                    try:
                        response=session.get(url,timeout=25);response.raise_for_status()
                        cache[url]=roster_positions(response.text)
                    except requests.RequestException as exc:cache[url]=str(exc)[:180]
                    time.sleep(1)
                data=cache[url]
                if isinstance(data,str):status,observed,reason="unverified","","source_unavailable: "+data
                else:
                    observed=";".join(sorted(data.get(row["bref_id"],set())))
                    status="supported" if observed==row["position"] else ("exception" if observed else "unverified")
                    reason="exact_2026_27_roster_cell" if status=="supported" else "missing_or_mismatched_roster_position"
            results.append({"nba_player_id":row["nba_player_id"],"bref_id":row["bref_id"],"expected_position":row["position"],"roster_url":url,"observed_position":observed,"status":status,"reason":reason,"formal_approval":"pending"})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    print("SEVEN_PLAYER_LIVE_ROSTER",json.dumps({"checked":7,"supported":sum(r["status"]=="supported" for r in results),"exceptions":sum(r["status"]=="exception" for r in results),"unverified":sum(r["status"]=="unverified" for r in results),"formal_approvals":0,"published":False}))

if __name__=="__main__":main()
