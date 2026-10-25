"""Read-only validation of the 11-player targeted review packet.

Usage: python scripts/validate_targeted_identity_review.py PATH_TO_REVIEW.csv
This script never approves identities or edits the verified crosswalk.
"""
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_POSITIONS = {"PG", "SG", "SF", "PF", "C"}
EXPECTED_REPORT = Path("reports/targeted_coverage_exceptions_2027.json")
REQUIRED = ("nba_player_id", "review_decision", "verified_bref_id",
            "verified_2026_27_position", "evidence_url")
BANNED_HOSTS = {"nba.com", "www.nba.com", "basketball-reference.com",
                "www.basketball-reference.com", "github.com",
                "www.github.com", "raw.githubusercontent.com"}
def validate(packet, expected_ids):
    issues = []
    seen = set()
    for number, row in enumerate(packet, start=2):
        pid = row["nba_player_id"].strip()
        if pid in seen:
            issues.append({"row": number, "nba_player_id": pid, "reason": "duplicate ID"})
        seen.add(pid)
        if pid not in expected_ids:
            issues.append({"row": number, "nba_player_id": pid, "reason": "not in audit exceptions"})
        decision = row["review_decision"].strip().lower()
        if decision not in {"pending", "verified", "rejected"}:
            issues.append({"row": number, "nba_player_id": pid, "reason": "invalid review decision"})
        if decision == "verified":
            bref = row["verified_bref_id"].strip()
            position = row["verified_2026_27_position"].strip()
            url = row["evidence_url"].strip()
            parsed = urlparse(url)
            if not bref or not bref.replace("_", "").isalnum():
                issues.append({"row": number, "nba_player_id": pid, "reason": "missing or malformed BRef ID"})
            if position not in ALLOWED_POSITIONS:
                issues.append({"row": number, "nba_player_id": pid, "reason": "missing precise season position"})
            if parsed.scheme != "https" or not parsed.hostname or parsed.hostname.lower() in BANNED_HOSTS:
                issues.append({"row": number, "nba_player_id": pid, "reason": "independent HTTPS evidence URL required"})
            if not row.get("review_notes", "").strip():
                issues.append({"row": number, "nba_player_id": pid, "reason": "review notes required"})
    for pid in sorted(expected_ids - seen):
        issues.append({"row": None, "nba_player_id": pid, "reason": "missing audit player"})
    return issues

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/validate_targeted_identity_review.py review.csv")
    report = json.loads(EXPECTED_REPORT.read_text(encoding="utf-8"))
    expected = {str(p["nba_player_id"]) for p in report["unmatched_candidates"]}
    with Path(sys.argv[1]).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = set(REQUIRED) - set(reader.fieldnames or [])
        if missing:
            raise SystemExit("Missing columns: " + ", ".join(sorted(missing)))
        packet = list(reader)
    issues = validate(packet, expected)
    counts = {key: sum(row["review_decision"].strip().lower() == key for row in packet)
              for key in ("pending", "verified", "rejected")}
    result = {"expected_players": len(expected), "submitted_rows": len(packet),
              "review_counts": counts, "issues": issues, "ready_for_independent_review": not issues,
              "crosswalk_changed": False, "publication_ready": False,
              "warning": "Syntactic evidence checks are not proof of identity; independent manual verification is still required."}
    print(json.dumps(result, indent=2))
    if issues:
        raise SystemExit(1)
if __name__ == "__main__":
    main()
