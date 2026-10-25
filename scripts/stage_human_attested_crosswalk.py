"""Stage user-attested approvals for validation; never alter the live crosswalk."""
import csv
import json
from pathlib import Path
from publish_verified_positions import validate_crosswalk_source, validate_independent_evidence, POSITIONS

PROPOSAL = Path("reports/proposed_verified_player_ids_2027.csv")
SEASON_EVIDENCE = Path("reports/season_position_evidence_2027.csv")
OUTPUT = Path("reports/human_attested_crosswalk_2027.csv")
EXCEPTIONS = Path("reports/human_attested_crosswalk_exceptions_2027.csv")
REVIEWER = "eec757"
REVIEW_DATE = "2026-10-25"
EXPECTED_NEW = 362
REVIEWED_IDS = Path("data/reviewed_player_ids_2027.txt")

def stage(proposal, evidence, reviewed_ids):
    supported = {(r["nba_player_id"], r["bref_id"]) for r in evidence if r["status"] == "supported"}
    rows, exceptions = [], []
    seen_nba, seen_bref = set(), set()
    newly_attested = 0
    for original in proposal:
        row = dict(original)
        pid, bref = row["nba_player_id"], row["bref_id"]
        was_approved = row.get("verified", "").strip().lower() == "true"
        if not was_approved and pid in reviewed_ids:
            row["reviewed_by"] = REVIEWER
            row["reviewed_on"] = REVIEW_DATE
            row["verified"] = "true"
            newly_attested += 1
        try:
            if (pid, bref) not in supported:
                raise ValueError("Missing precise 2026-27 roster position support")
            if row["position"] not in POSITIONS:
                raise ValueError("Invalid precise position")
            validate_crosswalk_source(row["verification_source"])
            validate_independent_evidence(row)
            if pid in seen_nba or bref in seen_bref:
                raise ValueError("Duplicate NBA or Basketball-Reference identity")
            seen_nba.add(pid)
            seen_bref.add(bref)
        except (KeyError, ValueError) as error:
            exceptions.append({"nba_player_id":pid, "bref_id":bref, "reason":str(error)})
        rows.append(row)
    if newly_attested != EXPECTED_NEW:
        exceptions.append({"nba_player_id":"", "bref_id":"", "reason":f"Expected {EXPECTED_NEW} newly attested candidates, got {newly_attested}"})
    return rows, exceptions, newly_attested

def main():
    with PROPOSAL.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        proposal = list(reader)
    with SEASON_EVIDENCE.open(newline="", encoding="utf-8") as f:
        evidence = list(csv.DictReader(f))
    if not REVIEWED_IDS.exists():
        raise ValueError("Immutable list of the 362 reviewed NBA IDs is required; current roster candidates must not be assumed reviewed")
    reviewed_ids = {line.strip() for line in REVIEWED_IDS.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
    if len(reviewed_ids) != EXPECTED_NEW:
        raise ValueError(f"Expected {EXPECTED_NEW} distinct reviewed NBA IDs; got {len(reviewed_ids)}")
    rows, exceptions, new = stage(proposal, evidence, reviewed_ids)
    proposed_ids = {r["nba_player_id"] for r in proposal}
    for missing in sorted(reviewed_ids - proposed_ids):
        exceptions.append({"nba_player_id":missing,"bref_id":"","reason":"Previously reviewed ID absent from current proposal"})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with EXCEPTIONS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nba_player_id","bref_id","reason"])
        writer.writeheader()
        writer.writerows(exceptions)
    # Fail closed: do not even stage an approval CSV if validation is incomplete.
    if exceptions:
        print("HUMAN_ATTESTED_CROSSWALK", json.dumps({"newly_attested":new, "exceptions":len(exceptions), "staged":False, "published":False}))
        raise ValueError("Attested candidate evidence has exceptions; see exception report")
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("HUMAN_ATTESTED_CROSSWALK", json.dumps({"newly_attested":new, "total":len(rows), "reviewer":REVIEWER, "review_date":REVIEW_DATE, "staged":True, "published":False, "live_crosswalk_modified":False, "output":str(OUTPUT)}))

if __name__ == "__main__":
    main()
