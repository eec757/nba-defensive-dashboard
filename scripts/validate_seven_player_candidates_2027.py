"""Read-only structural validation of seven unapproved crosswalk candidates."""
import csv
import json
from pathlib import Path
from urllib.parse import urlparse
from publish_verified_positions import validate_crosswalk_source, POSITIONS

SOURCE=Path("reports/2027_seven_player_unapproved_crosswalk_candidates.csv")
OUT=Path("reports/2027_seven_player_candidate_validation.csv")
EXPECTED={"1626171","1641713","1641842","1643515","1629057","1642383","1641747"}

def validate(r):
    errors=[]
    pid=r.get("nba_player_id","").strip();bref=r.get("bref_id","").strip()
    if not pid.isdigit() or pid not in EXPECTED:errors.append("unexpected_nba_id")
    if not bref or not bref.isalnum():errors.append("invalid_bref_id")
    if r.get("position") not in POSITIONS:errors.append("invalid_position")
    if r.get("verified","").lower()!="false":errors.append("not_unapproved")
    if r.get("reviewed_by") or r.get("reviewed_on"):errors.append("unexpected_formal_approval_metadata")
    if r.get("nba_profile_url")!=f"https://www.nba.com/player/{pid}":errors.append("nba_profile_url_mismatch")
    if not bref or r.get("bref_profile_url")!=f"https://www.basketball-reference.com/players/{bref[:1]}/{bref}.html":errors.append("bref_profile_url_mismatch")
    try:validate_crosswalk_source(r.get("verification_source",""))
    except ValueError:errors.append("invalid_independent_evidence_url_structure")
    source=urlparse(r.get("position_source",""))
    if source.scheme!="https" or source.hostname!="www.basketball-reference.com" or not source.path.endswith("/2027.html"):
        errors.append("invalid_season_position_source_url_structure")
    return errors

def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    if len(rows)!=7 or {r["nba_player_id"] for r in rows}!=EXPECTED:raise ValueError("Expected exactly seven distinct candidate IDs")
    results=[]
    for r in rows:
        errors=validate(r)
        results.append({"nba_player_id":r["nba_player_id"],"bref_id":r["bref_id"],"position":r["position"],"structure_valid":"yes" if not errors else "no","formal_approval":"pending","independent_evidence_content_review":"required","position_source_content_review":"required","issues":";".join(errors)})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    print("SEVEN_PLAYER_CANDIDATE_VALIDATION",json.dumps({"candidates":7,"structurally_valid":sum(x["structure_valid"]=="yes" for x in results),"formally_approved":0,"source_content_verified":False,"published":False}))
    if any(r["issues"] for r in results):raise ValueError("Candidate structural validation failed")

if __name__=="__main__":main()
