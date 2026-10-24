"""Validate availability and game-log overlap for 2026-27 roster positions."""
import os
import tempfile
import requests
import duckdb

URL = "https://github.com/sportsdataverse/sportsdataverse-data/releases/download/nba_stats_rosters/rosters_2027.parquet"
CATALOG = "https://basketball-data.billmill.org/nba/nba.duckdb"

def main():
    response = requests.get(URL, timeout=35)
    print(f"Roster download HTTP: {response.status_code}; bytes: {len(response.content)}", flush=True)
    response.raise_for_status()
    if response.content[:4] != b"PAR1":
        raise ValueError("Roster download is not Parquet")
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "roster.parquet")
        with open(path, "wb") as f:
            f.write(response.content)
        db = duckdb.connect()
        columns = [r[0] for r in db.execute("DESCRIBE SELECT * FROM read_parquet(?)", [path]).fetchall()]
        print("Roster columns:", columns, flush=True)
        required = {"player_id", "team_id", "position"}
        if not required.issubset(columns):
            raise ValueError(f"Missing required columns: {required - set(columns)}")
        print("Roster rows, players, teams:", db.execute(
            "SELECT count(*), count(DISTINCT player_id), count(DISTINCT team_id) FROM read_parquet(?)", [path]
        ).fetchall(), flush=True)
        print("Listed positions:", db.execute(
            "SELECT position, count(*) FROM read_parquet(?) GROUP BY 1 ORDER BY 1", [path]
        ).fetchall(), flush=True)
        db.execute("INSTALL httpfs; LOAD httpfs;")
        db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
        print("Game-log columns:", [r[0] for r in db.execute("DESCRIBE SELECT * FROM nba.player_game_logs").fetchall()], flush=True)
        print("Game-log sample:", db.execute("SELECT * FROM nba.player_game_logs WHERE season=2027 LIMIT 1").fetchall(), flush=True)
        print("Roster sample:", db.execute("SELECT player_id, team_id, position FROM read_parquet(?) LIMIT 5", [path]).fetchall(), flush=True)

if __name__ == "__main__":
    main()
