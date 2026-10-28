"""Reconcile user review, exact live ID evidence, and candidate rows without approval."""
import csv
import json
from pathlib import Path

ROOT=Path("reports")
def read(name):
    with (ROOT/name).open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def main():
    attest=read("2027_seven_player_user_review_attestation.csv")
    candidates=read("2027_seven_player_unapproved_crosswalk_candidates.csv")
    live=read("2027_seven_player_live_wikidata_checks.csv")
    structural=read("2027_seven_player_candidate_validation.csv")
    sources=(attest,candidates,live,structural)
    if any(len(rows)!=7 or len({r["nba_player_id"] for r in rows})!=7 for rows in sources):
        raise ValueError("Expected seven distinct IDs in each input")
    maps=[{r["nba_player_id"]:r for r in rows} for rows in sources]
    if any(set(m)!=set(maps[0]) for m in maps[1:]):raise ValueError("Candidate set drift")
    output=[]
    for pid in sorted(maps[0]):
        a,c,l,s=(m[pid] for m in maps)
        blockers=[]
        if (a["bref_id"],a["season_primary_position"])!=(c["bref_id"],c["position"]):blockers.append("attestation_candidate_conflict")
        if a.get("review_attestation")!="user_confirmed_all_seven_in_chat":blockers.append("user_attestation_missing")
        if a.get("formal_approval_status")!="pending_provenance":blockers.append("unexpected_formal_status")
        if (l.get("result")!="both_ids_match" or l.get("bref_id")!=c["bref_id"]):blockers.append("live_dual_id_not_matched")
        if s.get("structure_valid")!="yes":blockers.append("candidate_structure_invalid")
        if c.get("verified")!="false":blockers.append("candidate_not_pending")
        output.append({"nba_player_id":pid,"bref_id":c["bref_id"],"position":c["position"],"user_attestation":"recorded","wikidata_dual_id":"matched" if l.get("result")=="both_ids_match" else "not_matched","candidate_structure":s.get("structure_valid",""),"formal_approval":"pending","remaining_requirement":"independent human approval provenance and source-content position signoff","reconciliation_issues":";".join(blockers)})
    out=ROOT/"2027_seven_player_provenance_reconciliation.csv"
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    issues=sum(bool(r["reconciliation_issues"]) for r in output)
    print("SEVEN_PLAYER_PROVENANCE_RECONCILIATION",json.dumps({"reconciled":7,"issues":issues,"formal_approvals":0,"published":False}))
    if issues:raise ValueError("Review and evidence provenance reconciliation failed")

if __name__=="__main__":main()
