"""Check source freshness without weakening coverage or publishing unverified data.

A completed reference game is a minimum freshness witness, not a full-season
completeness guarantee. Reports are informational and always unpublished.
"""
import json
from pathlib import Path

SOURCE = Path("reports/2027_source_freshness.json")
OUT = Path("reports/2027_source_readiness.json")

def evaluate(source):
    expected = source.get("expected_completed_phoenix_game_id")
    game_present = source.get("expected_game_present_in_regular_season_catalog") is True
    phoenix_present = source.get("expected_game_has_phoenix_opponent_rows") is True
    missing = not (game_present and phoenix_present)
    return {
        "source_checked_at_utc": source.get("checked_at_utc"),
        "source_catalog": source.get("catalog"),
        "reference_game_id": expected,
        "reference_game_present": game_present,
        "phoenix_opponent_rows_present": phoenix_present,
        "source_reference_freshness_pass": not missing,
        "requires_source_refresh": missing,
        "publication_ready": False,
        "position_policy": "season_roster_primary_game_roles_separate",
        "reason": "Missing completed reference game in source snapshot" if missing else
                  "Reference game present; full source completeness and identity/coverage gates still require independent checks",
    }

def main():
    source=json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("season") != 2027 or not source.get("expected_completed_phoenix_game_id"):
        raise ValueError("Invalid 2027 source freshness input")
    result=evaluate(source)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("SOURCE_READINESS",json.dumps(result))

if __name__=="__main__":main()
