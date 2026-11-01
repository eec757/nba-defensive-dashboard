"""Read-only reconciliation of seven user attestations with approval requirements."""
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ATTESTATION=Path("reports/2027_seven_player_user_review_attestation.csv")
APPROVED=Path("data/verified_player_ids_2027.csv")
OUT=Path("reports/2027_seven_player_attestation_readiness.csv")
REQUIRED=("nba_profile_url","bref_profile_url","position_source","verification_source","reviewed_by","reviewed_on")
DISALLOWED={"nba.com","www.nba.com","basketball-reference.com","www.basketball-reference.com","github.com","www.github.com","raw.githubusercontent.com","gist.github.com"}

def main():
    with ATTESTATION.open(newline="",encoding="utf-8") as f: attest=list(csv.DictReader(f))
    with APPROVED.open(newline="",encoding="utf-8") as f: crosswalk={r["nba_player_id"]:r for r in csv.DictReader(f)}
    if len(attest)!=7 or len({r["nba_player_id"] for r in attest})!=7:
        raise ValueError("Expected seven distinct reviewed player IDs")
    output=[]
    for a in attest:
        r=crosswalk.get(a["nba_player_id"])
        blockers=[]
        if a["formal_approval_status"]!="pending_provenance":
            raise ValueError("Attestation status changed unexpectedly; review manually")
        if r is None: blockers.append("not_in_verified_crosswalk")
        else:
            if r["bref_id"]!=a["bref_id"] or r["position"]!=a["season_primary_position"]:
                blockers.append("crosswalk_identity_or_position_conflict")
            blockers.extend("missing_"+k for k in REQUIRED if not (r.get(k) or "").strip())
            url=urlparse((r.get("verification_source") or "").strip())
            if url.scheme!="https" or not url.hostname or url.hostname.lower() in DISALLOWED:
                blockers.append("independent_identity_evidence_not_eligible")
            if r.get("verified","").lower()!="true":blockers.append("formal_approval_not_recorded")
        output.append({"nba_player_id":a["nba_player_id"],"bref_id":a["bref_id"],"position":a["season_primary_position"],"user_review_attested":"yes","formal_approval_ready":"yes" if not blockers else "no","blockers":";".join(blockers)})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    print("SEVEN_PLAYER_ATTESTATION_READINESS",json.dumps({"attested":7,"formally_approved":sum(x["formal_approval_ready"]=="yes" for x in output),"pending":sum(x["formal_approval_ready"]=="no" for x in output),"published":False}))

if __name__=="__main__":main()
