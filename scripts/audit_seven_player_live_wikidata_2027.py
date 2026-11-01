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
    expected={"1626171","1641713","1641842","1643515","1629057","1642383","1641747"}
    with Path("data/verified_player_ids_2027.csv").open(newline="",encoding="utf-8") as f:
        approved={r["nba_player_id"] for r in csv.DictReader(f) if r.get("verified","").strip().lower()=="true"}
    pending=expected-approved
    if len(rows)!=len(pending) or {r["nba_player_id"] for r in rows}!=pending:
        raise ValueError("Expected exact unapproved candidate IDs after approved exclusions")
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
    print("SEVEN_PLAYER_LIVE_WIKIDATA",json.dumps({"checked":len(rows),"already_approved_omitted":len(expected & approved),"exact_dual_id_matches":passed,"unresolved":len(rows)-passed,"human_approved":0,"published":False}))
    if passed!=len(rows):raise ValueError("Not all live Wikidata identity statements match; do not approve")

if __name__=="__main__":main()
