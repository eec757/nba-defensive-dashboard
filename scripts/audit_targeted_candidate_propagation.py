"""Read-only audit: do targeted review candidates reach generated game-log identity staging?"""
import csv
import json
from pathlib import Path

TARGET = Path("reports/2027_targeted_identity_evidence_reconstruction.csv")
STAGED = Path("reports/missing_game_log_identity_evidence_2027.json")
OUTPUT = Path("reports/2027_targeted_candidate_propagation.json")

def build(target_rows, staged_players):
    by_id = {str(p["nba_player_id"]): p for p in staged_players}
    results = []
    for row in target_rows:
        pid = row["nba_player_id"]
        staged = by_id.get(pid)
        actual = sorted({str(c.get("bref_id", "")) for c in (staged or {}).get("identity_candidates", []) if c.get("bref_id")})
        expected = row["candidate_bref_id"]
        results.append({
            "nba_player_id": pid,
            "candidate_bref_id": expected,
            "staged_bref_ids": actual,
            "status": "exact_candidate_match" if expected in actual and len(actual) == 1
                      else "not_in_unmatched_staging" if staged is None
                      else "candidate_not_propagated",
            "approval_status": row["approval_status"],
        })
    return {"results": results, "candidate_mismatches": [r for r in results if r["status"] == "candidate_not_propagated"],
            "published": False, "crosswalk_modified": False,
            "warning": "Candidate equality is not proof of independent identity verification or publication readiness."}

def main():
    with TARGET.open(newline="", encoding="utf-8") as f:
        targets = list(csv.DictReader(f))
    staged = json.loads(STAGED.read_text(encoding="utf-8"))
    result = build(targets, staged["players"])
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("TARGETED_CANDIDATE_PROPAGATION", json.dumps(result))
if __name__ == "__main__":
    main()
