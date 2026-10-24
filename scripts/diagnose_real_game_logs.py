"""Read-only diagnostic of live NBA game-log aggregation.

This script never marks identities verified and never publishes dashboard data.
"""
import json
import duckdb
from publish_verified_positions import CATALOG, TEAM_IDS, summarize_position_rows

def main():
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows = db.execute("""
        SELECT p.player_id,p.opp_team_id,p.game_id,p.pts,p.reb,p.ast,
               p.fgm,p.fga,p.fg3m,p.fg3a
        FROM nba.player_game_logs p
        JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    if not rows:
        raise ValueError("No 2026-27 regular-season game logs available")
    totals, games, covered, all_rows = summarize_position_rows(rows, {}, TEAM_IDS)
    if totals or covered:
        raise AssertionError("Unverified identities unexpectedly aggregated")
    active = {team: len(ids) for team, ids in games.items() if ids}
    if len(active) != 30:
        raise ValueError(f"Expected game logs for 30 teams; found {len(active)}")
    if any(all_rows[team] <= 0 for team in TEAM_IDS):
        raise ValueError("Missing opponent player-game rows for one or more teams")
    report = {
        "season": "2026-27",
        "player_game_rows": len(rows),
        "active_defending_teams": len(active),
        "defending_team_games": dict(sorted(active.items())),
        "unique_player_ids": len({str(row[0]) for row in rows}),
        "total_defending_team_games": sum(active.values()),
        "opponent_player_rows_by_team": dict(sorted(all_rows.items())),
        "unknown_opponent_ids": [],
        "position_statistics_published": False,
        "note": "Read-only data diagnostics; no player positions inferred or verified."
    }
    print("REAL_GAME_LOG_DIAGNOSTIC", json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
