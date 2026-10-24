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
