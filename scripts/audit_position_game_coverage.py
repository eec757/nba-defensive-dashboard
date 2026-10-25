"""Read-only coverage report for proposed season-verified player identities.

This report is informational, never grants approval or publishes defensive stats.
Unknown player positions count against every relevant position's denominator
rather than being silently excluded.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

PROPOSAL=Path("reports/proposed_verified_player_ids_2027.csv")
EVIDENCE=Path("reports/season_position_evidence_2027.csv")
OUT=Path("reports/position_identity_coverage_2027.json")

def main():
    with PROPOSAL.open(newline="",encoding="utf-8") as f:
        proposed=list(csv.DictReader(f))
    with EVIDENCE.open(newline="",encoding="utf-8") as f:
        evidence=list(csv.DictReader(f))
    approved={(r["nba_player_id"],r["bref_id"]) for r in evidence if r["status"]=="supported"}
    candidate={(r["nba_player_id"],r["bref_id"]) for r in proposed}
    verified=approved & candidate
    report={"proposed_records":len(proposed),"season_position_supported_records":len(verified),
            "unsupported_records":len(proposed)-len(verified),
            "player_record_support_pct":round(100*len(verified)/len(proposed),2) if proposed else 0,
            "leaguewide_player_game_coverage_pct":None,
            "defending_team_player_game_coverage_pct":None,
            "defending_team_position_player_game_coverage_pct":None,
            "publication_ready":False,
            "reason":"Player identity/position evidence alone cannot establish player-game or defending-team/position coverage. A validated player-game-to-defender dataset is required."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("POSITION_GAME_COVERAGE_READINESS",json.dumps(report))

if __name__=="__main__":
    main()
