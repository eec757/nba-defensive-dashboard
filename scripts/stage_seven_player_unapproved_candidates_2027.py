"""Stage seven reviewed candidates as UNAPPROVED crosswalk rows, fail closed."""
import csv
import json
from pathlib import Path
from publish_verified_positions import validate_crosswalk_source, POSITIONS

ATTEST=Path("reports/2027_seven_player_user_review_attestation.csv")
CURRENT=Path("data/verified_player_ids_2027.csv")
OUTPUT=Path("reports/2027_seven_player_unapproved_crosswalk_candidates.csv")
EXCEPTIONS=Path("reports/2027_seven_player_candidate_exceptions.csv")
ROSTERS={"1626171":"MIA","1641713":"MEM","1641842":"DET","1643515":"CHO","1629057":"POR","1642383":"DAL","1641747":"DEN"}
QIDS={"1626171":"Q19667582","1641713":"Q115492105","1641842":"Q116407941","1643515":"Q133691210","1629057":"Q28151848","1642383":"Q117262884","1641747":"Q115492041"}

def main():
    with ATTEST.open(newline="",encoding="utf-8") as f: reviews=list(csv.DictReader(f))
    with CURRENT.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f); fields=reader.fieldnames; current=list(reader)
    if len(reviews)!=7 or {r["nba_player_id"] for r in reviews}!=set(ROSTERS):
        raise ValueError("Attested seven-player set does not match reviewed identities")
    existing_nba={r["nba_player_id"] for r in current}
    existing_bref={r["bref_id"] for r in current}
    exceptions=[]; staged=[]
    for a in reviews:
        pid=a["nba_player_id"];bref=a["bref_id"];pos=a["season_primary_position"]
        reason=[]
        if pid in existing_nba or bref in existing_bref:reason.append("already_in_crosswalk_review_conflict")
        if pos not in POSITIONS or not bref or not bref.isalnum():reason.append("invalid_position_or_bref_id")
        if a["formal_approval_status"]!="pending_provenance":reason.append("unexpected_attestation_status")
        evidence=f"https://www.wikidata.org/wiki/{QIDS[pid]}"
        try:validate_crosswalk_source(evidence)
        except ValueError as e:reason.append(str(e))
        row={"nba_player_id":pid,"bref_id":bref,"position":pos,"verification_source":evidence,"verified":"false","nba_profile_url":f"https://www.nba.com/player/{pid}","bref_profile_url":f"https://www.basketball-reference.com/players/{bref[0]}/{bref}.html","reviewed_by":"","reviewed_on":"","position_source":f"https://www.basketball-reference.com/teams/{ROSTERS[pid]}/2027.html"}
        if reason:exceptions.append({"nba_player_id":pid,"reason":";".join(reason)})
        staged.append(row)
    EXCEPTIONS.parent.mkdir(parents=True,exist_ok=True)
    with EXCEPTIONS.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["nba_player_id","reason"]);w.writeheader();w.writerows(exceptions)
    if exceptions:raise ValueError(f"Seven-player staging blocked by {len(exceptions)} exceptions")
    with OUTPUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(staged)
    print("SEVEN_PLAYER_UNAPPROVED_STAGING",json.dumps({"candidates":len(staged),"verified_true":0,"exceptions":0,"live_crosswalk_modified":False,"publication_ready":False}))

if __name__=="__main__":main()
