"""Read-only checklist for crosswalk approvals; never changes verified flags."""
import csv
import json
from pathlib import Path

SOURCE = Path("data/verified_player_ids_2027.csv")
OUTPUT = Path("reports/identity_approval_readiness_2027.csv")
REQUIRED = ("nba_profile_url", "bref_profile_url", "position_source", "reviewed_by", "reviewed_on")

def main():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    report = []
    for row in rows:
        missing = [field for field in REQUIRED if not (row.get(field) or "").strip()]
        report.append({
            "nba_player_id": row["nba_player_id"],
            "bref_id": row["bref_id"],
            "position": row["position"],
            "position_source": row.get("position_source", ""),
            "verified": row["verified"],
            "missing_fields": ";".join(missing),
            "review_ready": "yes" if not missing else "no",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(report[0]) if report else [
            "nba_player_id", "bref_id", "position", "position_source", "verified", "missing_fields", "review_ready"
        ])
        writer.writeheader()
        writer.writerows(report)
    print("IDENTITY_APPROVAL_READINESS", json.dumps({
        "entries": len(report),
        "metadata_complete": sum(r["review_ready"] == "yes" for r in report),
        "approved": sum(r["verified"].strip().lower() == "true" for r in report),
        "report": str(OUTPUT),
        "warning": "Metadata completeness does not establish independent identity verification."
    }))

if __name__ == "__main__":
    main()
