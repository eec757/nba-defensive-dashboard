"""Read-only, fail-closed readiness assessment for Alpha Diallo evidence."""
import csv
import json
from pathlib import Path

NBA_ID = "1643813"
TARGET = Path("reports/2027_targeted_identity_evidence_reconstruction.csv")
OFFICIAL = Path("reports/2027_official_nba_identity_evidence.csv")
POSITION = Path("reports/2027_diallo_sg_position_evidence.csv")
STAGED = Path("reports/missing_game_log_identity_evidence_2027.json")
OUTPUT = Path("reports/2027_diallo_evidence_readiness.json")

def main():
    def rows(path):
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    target = [r for r in rows(TARGET) if r["nba_player_id"] == NBA_ID]
    official = [r for r in rows(OFFICIAL) if r["nba_player_id"] == NBA_ID]
    positions = [r for r in rows(POSITION) if r["nba_player_id"] == NBA_ID]
    players = json.loads(STAGED.read_text(encoding="utf-8"))["players"]
    staged = [p for p in players if str(p["nba_player_id"]) == NBA_ID]
    if len(target) != 1 or len(official) != 1 or len(staged) != 1:
        raise SystemExit("Expected exactly one Diallo record in each required source")
    candidate = target[0]["candidate_bref_id"]
    staged_bref = sorted({str(c.get("bref_id")) for c in staged[0].get("identity_candidates", []) if c.get("bref_id")})
    official_present = any(e.get("url") == official[0]["evidence_url"] for e in staged[0].get("official_nba_identity_evidence", []))
    season_sg = [r for r in positions if r.get("source_position") == "SG" and r.get("temporal_scope") == "2026-27" and r.get("evidence_status") == "verified"]
    report = {
        "nba_player_id": NBA_ID, "candidate_bref_id": candidate, "candidate_position": target[0]["candidate_position"],
        "official_nba_evidence_propagated": official_present,
        "candidate_bref_id_in_wikidata_staging": candidate in staged_bref,
        "season_specific_sg_evidence_verified": bool(season_sg),
        "exact_identity_link_independently_verified": False,
        "ready_for_automatic_publication": False,
        "crosswalk_modified": False,
        "next_evidence_needed": ["Independent exact NBA-ID to Basketball-Reference-ID link",
                                 "Reconcile season-specific SG versus G/SF roster classifications"],
    }
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("DIALLO_EVIDENCE_READINESS", json.dumps(report))
    if not official_present:
        raise SystemExit("Official NBA evidence not present in staged record")

if __name__ == "__main__":
    main()
