"""Recover the precise reviewed NBA IDs from the original audit review packet.

Usage: python scripts/recover_reviewed_player_ids.py path/to/original/human_identity_review_packet_2027.csv
Never infer the reviewed set from today's changing roster.
"""
import csv
import sys
from pathlib import Path

EXPECTED = 362
DEST = Path("data/reviewed_player_ids_2027.txt")

def recover(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"nba_player_id", "review_decision", "bref_id", "proposed_position"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Original packet missing columns: {sorted(required - set(reader.fieldnames or []))}")
        rows = list(reader)
    pending = [r for r in rows if r["review_decision"] == "pending_human_review"]
    ids = [r["nba_player_id"].strip() for r in pending]
    if len(pending) != EXPECTED or len(set(ids)) != EXPECTED or any(not pid.isdigit() for pid in ids):
        raise ValueError(f"Expected exactly {EXPECTED} distinct numeric pending player IDs in original packet")
    if any(r["proposed_position"] not in {"PG", "SG", "SF", "PF", "C"} or not r["bref_id"].strip() for r in pending):
        raise ValueError("Original review packet contains incomplete identity or position")
    if any(r["review_decision"] not in {"pending_human_review", "existing_approval"} for r in rows):
        raise ValueError("Unexpected review status")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text("# NBA IDs from original 362-player human review packet; eec757 attested 2026-10-25\n" + "\n".join(sorted(ids, key=int)) + "\n", encoding="utf-8")
    print(f"Recovered {len(ids)} distinct reviewed IDs into {DEST}; no approvals or dashboard files modified.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Provide path to the ORIGINAL 362-pending-player review packet CSV")
    recover(sys.argv[1])
