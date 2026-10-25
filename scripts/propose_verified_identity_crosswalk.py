"""Prepare a reviewable crosswalk promotion proposal; never modify live approvals."""
import csv
import json
from pathlib import Path
from urllib.parse import urlparse
from publish_verified_positions import validate_crosswalk_source, validate_independent_evidence, POSITIONS

CURRENT=Path("data/verified_player_ids_2027.csv")
MATCHES=Path("reports/wikidata_exact_matches_2027.csv")
PROPOSAL=Path("reports/proposed_verified_player_ids_2027.csv")
EXCEPTIONS=Path("reports/identity_promotion_exceptions_2027.csv")
REVIEWER="eec757"
REVIEW_DATE="2026-10-24"

def main():
    with CURRENT.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames
        current=list(reader)
    with MATCHES.open(newline="",encoding="utf-8") as f:
        matches=list(csv.DictReader(f))
    if len(matches)!=362:
        raise ValueError(f"Expected 362 independently matched candidates; got {len(matches)}")
    result=list(current)
    existing_nba={r["nba_player_id"]:r for r in current}
    existing_bref={r["bref_id"]:r for r in current}
    exceptions=[]
    promoted=0
    for row in matches:
        pid,bref=row["nba_player_id"],row["bref_id"]
        source=row["verification_source"].replace("https://www.wikidata.org/entity/","https://www.wikidata.org/wiki/")
        proposed={
            "bref_id":bref,"nba_player_id":pid,"position":row["position"],
            "verification_source":source,"verified":"true",
            "nba_profile_url":row["nba_profile_url"],
            "bref_profile_url":row["bref_profile_url"],
            "reviewed_by":REVIEWER,"reviewed_on":REVIEW_DATE,
            "position_source":row["position_source"]
        }
        reason=""
        try:
            if row["verified"].lower()!="false":
                raise ValueError("Expected unapproved evidence staging row")
            if row["position"] not in POSITIONS:
                raise ValueError("Invalid position")
            if urlparse(source).hostname!="www.wikidata.org" or not urlparse(source).path.startswith("/wiki/Q"):
                raise ValueError("Evidence must be exact Wikidata entity")
            validate_crosswalk_source(source)
            validate_independent_evidence(proposed)
            if pid in existing_nba and existing_nba[pid]["bref_id"]!=bref:
                raise ValueError("Conflicting existing NBA ID")
            if bref in existing_bref and existing_bref[bref]["nba_player_id"]!=pid:
                raise ValueError("Conflicting existing BRef ID")
            if pid in existing_nba:
                previous=existing_nba[pid]
                if previous["verified"].lower()=="true":
                    continue
                result.remove(previous)
            result.append(proposed)
            existing_nba[pid]=proposed
            existing_bref[bref]=proposed
            promoted+=1
        except (ValueError,KeyError) as exc:
            reason=str(exc)
        if reason:
            exceptions.append({"nba_player_id":pid,"bref_id":bref,"reason":reason})
    PROPOSAL.parent.mkdir(parents=True,exist_ok=True)
    with PROPOSAL.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(result)
    with EXCEPTIONS.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["nba_player_id","bref_id","reason"])
        writer.writeheader()
        writer.writerows(exceptions)
    print("PROMOTION_EXCEPTION_SAMPLE",json.dumps(exceptions[:5]))
    print("IDENTITY_PROMOTION_PROPOSAL",json.dumps({
        "existing":len(current),"candidate_exact_matches":len(matches),
        "new_or_updated_approvals_in_proposal":promoted,"exceptions":len(exceptions),
        "proposed_total":len(result),"published":False,
        "warning":"Proposal only; live crosswalk and dashboard remain unchanged."}))
    if exceptions:
        raise ValueError("Promotion proposal has conflicts; review exception artifact")

if __name__=="__main__":
    main()
