"""Inspect candidate NBA player logs and position labels without changing dashboard data."""
import sys

import duckdb

CATALOG = "https://basketball-data.billmill.org/nba/nba.duckdb"


def main():
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    for year in (2026, 2027):
        print(f"\\nSeason {year-1}-{str(year)[-2:]}", flush=True)
        for name, query in (
            ("player games", "SELECT count(*) FROM nba.player_game_logs WHERE season = ?"),
            ("regular-season player games", """
                SELECT count(*) FROM nba.player_game_logs p
                JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
                WHERE p.season=? AND g.game_type='regular_season'
            """),
            ("positions from NBA player seasons", """
                SELECT position, count(*) AS players
                FROM nba.player_seasons
                WHERE season=?
                GROUP BY 1 ORDER BY 1
            """),
            ("2026-27 game-log player ID position coverage", """
                SELECT count(*) AS game_rows,
                       count(s.player_id) AS matched_rows,
                       count(CASE WHEN s.position IS NOT NULL AND trim(s.position) <> '' THEN 1 END) AS positioned_rows,
                       count(DISTINCT p.player_id) AS unique_players,
                       count(DISTINCT CASE WHEN s.position IS NOT NULL AND trim(s.position) <> '' THEN p.player_id END) AS positioned_players
                FROM nba.player_game_logs p
                JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
                LEFT JOIN nba.player_seasons s ON p.season=s.season AND p.player_id=s.player_id
                WHERE p.season=? AND g.game_type='regular_season'
            """),
            ("positions from EPM", """
                SELECT e.position, count(*) AS players
                FROM nba.epm e
                WHERE e.season=? AND e.season_type='regular_season'
                GROUP BY 1 ORDER BY 1
            """),
        ):
            try:
                rows = db.execute(query, [year]).fetchall()
                print(f"{name}: {rows}", flush=True)
            except Exception as exc:
                print(f"{name}: unavailable ({exc})", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Position source probe failed: {exc}", file=sys.stderr)
        sys.exit(1)
