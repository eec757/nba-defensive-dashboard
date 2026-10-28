"""Check actual Wikidata dual-ID statements for seven UNAPPROVED candidates."""
import csv
import json
from pathlib import Path
import requests
from audit_wikidata_identity_statements import check

SOURCE=Path("reports/2027_seven_player_unapproved_crosswalk_candidates.csv")
OUT=Path("reports/2027_seven_player_live_wikidata_checks.csv")

def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    if len(rows)!=7 or len({r["nba_player_id"] for r in rows})!=7:
        raise ValueError("Expected seven distinct unapproved candidates")
    report=[]
    with requests.Session() as session:
        for row in rows:
            if row.get("verified")!="false":raise ValueError("Candidate unexpectedly approved")
            result=check(row,session)
            if result is None:result={"result":"invalid_wikidata_url","detail":"Not a Wikidata entity"}
            report.append({"nba_player_id":row["nba_player_id"],"bref_id":row["bref_id"],"position":row["position"],"wikidata_entity":result.get("wikidata_entity",""),"nba_statement_match":result.get("nba_statement_match",""),"bref_statement_match":result.get("bref_statement_match",""),"result":result["result"],"detail":result.get("detail",""),"human_approval":"pending","publication_ready":"false"})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(report[0]));w.writeheader();w.writerows(report)
    passed=sum(r["result"]=="both_ids_match" for r in report)
    print("SEVEN_PLAYER_LIVE_WIKIDATA",json.dumps({"checked":7,"exact_dual_id_matches":passed,"unresolved":7-passed,"human_approved":0,"published":False}))
    if passed!=7:raise ValueError("Not all live Wikidata identity statements match; do not approve")

if __name__=="__main__":main()
