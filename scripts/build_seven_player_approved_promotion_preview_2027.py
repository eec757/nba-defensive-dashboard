"""Create an approved seven-player crosswalk PROMOTION PREVIEW only.

Never edits data/verified_player_ids_2027.csv or publishes analytics.
Requires owner authorization document, live dual-ID and roster evidence, and
a conflict-free merge with the current crosswalk.
"""
import csv
import json
from pathlib import Path
from publish_verified_positions import validate_crosswalk_source,validate_independent_evidence

ROOT=Path("reports")
APPROVAL=Path("docs/seven-player-owner-approval-2027.md")
CURRENT=Path("data/verified_player_ids_2027.csv")
OUT=ROOT/"2027_seven_player_approved_promotion_preview.csv"
IDS={"1626171","1641713","1641842","1643515","1629057","1642383","1641747"}
REVIEWER="eec757"
REVIEW_DATE="2026-10-28"

def load(path):
    with path.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        return reader.fieldnames,list(reader)

def main():
    approval=APPROVAL.read_text(encoding="utf-8")
    if "authenticated GitHub account ID 347254476" not in approval or "explicitly answered" not in approval:
        raise ValueError("Missing attributable owner authorization")
    fields,current=load(CURRENT)
    _,pending=load(ROOT/"2027_seven_player_unapproved_crosswalk_candidates.csv")
    _,ids=load(ROOT/"2027_seven_player_live_wikidata_checks.csv")
    _,rosters=load(ROOT/"2027_seven_player_live_roster_positions.csv")
    _,review=load(ROOT/"2027_seven_player_user_review_attestation.csv")
    def indexed(rows):
        d={r["nba_player_id"]:r for r in rows}
        if len(rows)!=7 or set(d)!=IDS:raise ValueError("Seven-player evidence set drift")
        return d
    p,i,s,a=map(indexed,(pending,ids,rosters,review))
    existing_nba={r["nba_player_id"] for r in current}
    existing_bref={r["bref_id"] for r in current}
    preview=[]
    for pid in sorted(IDS):
        row=dict(p[pid])
        if pid in existing_nba or row["bref_id"] in existing_bref:raise ValueError("Existing crosswalk conflict")
        if i[pid]["result"]!="both_ids_match" or i[pid]["bref_id"]!=row["bref_id"]:
            raise ValueError("Live identity check incomplete")
        if s[pid]["status"]!="supported" or s[pid]["observed_position"]!=row["position"]:
            raise ValueError("Live roster position check incomplete")
        if (a[pid]["bref_id"],a[pid]["season_primary_position"])!=(row["bref_id"],row["position"]):
            raise ValueError("Review attestation mismatch")
        if f"| {pid} | {row['bref_id']} | {row['position']} |" not in approval:
            raise ValueError("Owner approval document does not cover exact identity and position")
        row.update(verified="true",reviewed_by=REVIEWER,reviewed_on=REVIEW_DATE)
        validate_crosswalk_source(row["verification_source"])
        validate_independent_evidence(row)
        preview.append(row)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader();w.writerows(preview)
    print("SEVEN_PLAYER_APPROVED_PREVIEW",json.dumps({"preview_rows":7,"crosswalk_modified":False,"publication":False,"reviewer":REVIEWER,"source_evidence_checked":True}))

if __name__=="__main__":main()
