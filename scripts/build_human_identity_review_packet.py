"""Generate an unapproved, human-actionable player identity review packet."""
import csv
import json
from pathlib import Path

PROPOSAL = Path("reports/proposed_verified_player_ids_2027.csv")
EVIDENCE = Path("reports/season_position_evidence_2027.csv")
OUTPUT = Path("reports/human_identity_review_packet_2027.csv")
BATCH_DIR = Path("reports/human_review_batches_2027")
BATCH_SIZE = 25
FIELDS = ("nba_player_id", "bref_id", "proposed_position", "nba_profile_url",
          "bref_profile_url", "independent_identity_source", "season_position_source",
          "season_position_supported", "current_live_verified", "review_decision",
          "reviewer", "review_date", "review_notes")

def build_packet(proposal_rows, evidence_rows):
    evidence = {(r["nba_player_id"], r["bref_id"]): r for r in evidence_rows}
    result = []
    for row in proposal_rows:
        match = evidence.get((row["nba_player_id"], row["bref_id"]), {})
        approved = row.get("verified", "").strip().lower() == "true"
        result.append({
            "nba_player_id": row["nba_player_id"],
            "bref_id": row["bref_id"],
            "proposed_position": row.get("position", ""),
            "nba_profile_url": row.get("nba_profile_url", ""),
            "bref_profile_url": row.get("bref_profile_url", ""),
            "independent_identity_source": row.get("verification_source", ""),
            "season_position_source": row.get("position_source", ""),
            "season_position_supported": "yes" if match.get("status") == "supported" else "no",
            "current_live_verified": "yes" if approved else "no",
            "review_decision": "existing_approval" if approved else "pending_human_review",
            "reviewer": "",
            "review_date": "",
            "review_notes": "",
        })
    return result

def main():
    with PROPOSAL.open(newline="", encoding="utf-8") as f:
        proposal_rows = list(csv.DictReader(f))
    with EVIDENCE.open(newline="", encoding="utf-8") as f:
        evidence_rows = list(csv.DictReader(f))
    rows = build_packet(proposal_rows, evidence_rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    pending = [row for row in rows if row["review_decision"] == "pending_human_review"]
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    for offset in range(0, len(pending), BATCH_SIZE):
        batch = pending[offset:offset + BATCH_SIZE]
        target = BATCH_DIR / f"batch_{offset // BATCH_SIZE + 1:02d}.csv"
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(batch)
    print("HUMAN_REVIEW_PACKET", json.dumps({
        "rows": len(rows),
        "pending_human_review": sum(r["review_decision"] == "pending_human_review" for r in rows),
        "existing_approved": sum(r["current_live_verified"] == "yes" for r in rows),
        "output": str(OUTPUT),
        "review_batches": (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE,
        "batch_size": BATCH_SIZE,
        "published": False,
        "note": "Review fields are intentionally blank; this packet cannot approve or publish identities."
    }))

if __name__ == "__main__":
    main()
