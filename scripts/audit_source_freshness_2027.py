"""Read-only source snapshot freshness diagnostic; does not authorize publication."""
import json
from datetime import datetime, timezone
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG, TEAM_IDS

OUT = Path("reports/2027_source_freshness.json")
# Confirmed completed PHO-hosted GSW game on 2026-10-24.
REFERENCE_GAME = "0022600111"

def main():
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows = db.execute("""
        SELECT CAST(p.game_id AS VARCHAR), CAST(p.opp_team_id AS VARCHAR), COUNT(*)
        FROM nba.player_game_logs p JOIN nba.games g
          ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
        GROUP BY 1,2
        ORDER BY 1,2
    """).fetchall()
    if not rows:
        raise ValueError("No 2026-27 regular-season rows in source catalog")
    phx_id = str(TEAM_IDS["PHO"])
    phx_games = sorted({gid for gid, team, _ in rows if team == phx_id})
    all_games = sorted({gid for gid, _, _ in rows})
    report = {
        "checked_at_utc":datetime.now(timezone.utc).isoformat(),
        "catalog":CATALOG,"season":2027,
        "source_player_game_rows":sum(count for _,_,count in rows),
        "source_distinct_game_ids":len(all_games),
        "source_latest_game_id":all_games[-1],
        "phoenix_defended_game_ids":phx_games,
        "phoenix_defended_game_count":len(phx_games),
        "expected_completed_phoenix_game_id":REFERENCE_GAME,
        "expected_game_present_in_regular_season_catalog":REFERENCE_GAME in all_games,
        "expected_game_has_phoenix_opponent_rows":REFERENCE_GAME in phx_games,
        "source_snapshot_incomplete_against_reference":REFERENCE_GAME not in phx_games,
        "publication_ready":False,"crosswalk_modified":False,
        "note":"Snapshot completeness diagnostic only. A missing reference game does not justify inventing rows or overriding any coverage gate."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("SOURCE_FRESHNESS",json.dumps(report))

if __name__=="__main__":main()
