"""Fail-closed check that official NBA evidence reaches generated game-log staging."""
import csv
import json
from pathlib import Path

LEDGER = Path("reports/2027_official_nba_identity_evidence.csv")
STAGED = Path("reports/missing_game_log_identity_evidence_2027.json")
OUTPUT = Path("reports/2027_official_nba_evidence_propagation.json")

def check(ledger, players):
    by_id = {str(p["nba_player_id"]): p for p in players}
    results = []
    for row in ledger:
        pid = row["nba_player_id"].strip()
        player = by_id.get(pid)
        evidence = [] if player is None else player.get("official_nba_identity_evidence", [])
        matched = any(e.get("url") == row["evidence_url"] and
                      e.get("player_name") == row["player_name"] and
                      e.get("listed_position") == row["listed_position"] and
                      e.get("scope") == "nba_id_name_team_broad_position_only"
                      for e in evidence)
        results.append({"nba_player_id": pid,
                        "status": "propagated" if matched else "missing_or_mismatched",
                        "evidence_url": row["evidence_url"]})
    return {"results": results, "all_evidence_propagated": all(r["status"] == "propagated" for r in results),
            "publication_ready": False, "crosswalk_modified": False,
            "warning": "Official NBA guard designation does not establish exact SG or BRef ID."}

def main():
    with LEDGER.open(newline="", encoding="utf-8") as f:
        ledger = list(csv.DictReader(f))
    staged = json.loads(STAGED.read_text(encoding="utf-8"))
    result = check(ledger, staged["players"])
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("OFFICIAL_NBA_EVIDENCE_PROPAGATION", json.dumps(result))
    if not result["all_evidence_propagated"]:
        raise SystemExit("Official NBA evidence failed to propagate into staging")
if __name__ == "__main__":
    main()
