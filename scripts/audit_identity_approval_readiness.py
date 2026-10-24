"""Read-only checklist for crosswalk approvals; never changes verified flags."""
import csv
import json
from urllib.parse import urlparse
from pathlib import Path

SOURCE = Path("data/verified_player_ids_2027.csv")
OUTPUT = Path("reports/identity_approval_readiness_2027.csv")
REQUIRED = ("nba_profile_url", "bref_profile_url", "position_source", "verification_source", "reviewed_by", "reviewed_on")
DISALLOWED_EVIDENCE_HOSTS = {"nba.com", "www.nba.com", "basketball-reference.com", "www.basketball-reference.com", "github.com", "www.github.com", "raw.githubusercontent.com", "gist.github.com"}

def main():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    report = []
    for row in rows:
        missing = [field for field in REQUIRED if not (row.get(field) or "").strip()]
        evidence = (row.get("verification_source") or "").strip()
        parsed = urlparse(evidence)
        evidence_eligible = bool(parsed.scheme == "https" and parsed.hostname and parsed.hostname.lower() not in DISALLOWED_EVIDENCE_HOSTS)
        if evidence and not evidence_eligible:
            missing.append("independent_identity_linkage_evidence")
        report.append({
            "nba_player_id": row["nba_player_id"],
            "bref_id": row["bref_id"],
            "position": row["position"],
            "position_source": row.get("position_source", ""),
            "verified": row["verified"],
            "independent_evidence_url_eligible": "yes" if evidence_eligible else "no",
            "missing_fields": ";".join(missing),
            "review_ready": "yes" if not missing else "no",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(report[0]) if report else [
            "nba_player_id", "bref_id", "position", "position_source", "verified", "independent_evidence_url_eligible", "missing_fields", "review_ready"
        ])
        writer.writeheader()
        writer.writerows(report)
    print("IDENTITY_APPROVAL_READINESS", json.dumps({
        "entries": len(report),
        "metadata_complete": sum(r["review_ready"] == "yes" for r in report),
        "eligible_independent_evidence_urls": sum(r["independent_evidence_url_eligible"] == "yes" for r in report),
        "approved": sum(r["verified"].strip().lower() == "true" for r in report),
        "report": str(OUTPUT),
        "warning": "URL eligibility and metadata completeness do not establish independent identity verification."
    }))

if __name__ == "__main__":
    main()
