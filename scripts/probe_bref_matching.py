"""Diagnostic: Basketball-Reference roster IDs and NBA player-game ID bridge, OKC only."""
import re
import unicodedata
import requests
import duckdb
from probe_bref_league import Roster

CATALOG = "https://basketball-data.billmill.org/nba/nba.duckdb"

def normalize(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", value.casefold())

def main():
    response = requests.get("https://www.basketball-reference.com/teams/OKC/2027.html", timeout=25,
        headers={"User-Agent": "Mozilla/5.0 (compatible; NBA-Dashboard-Validation/1.0)"})
    print("HTTP status:", response.status_code, flush=True)
    response.raise_for_status()
    parser = Roster()
    parser.feed(response.text)
    print("Roster player count:", len(parser.rows), flush=True)
    print("Roster player IDs:", sum(bool(r.get("bref_id")) for r in parser.rows), flush=True)
    print("Roster sample:", [(r.get("player") or r.get("player_name"),r.get("bref_id"),r.get("pos")) for r in parser.rows[:5]], flush=True)
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    for table in ("players", "player_game_logs", "player_seasons"):
        try:
            print(table, "columns:", [x[0] for x in db.execute(f"DESCRIBE SELECT * FROM nba.{table}").fetchall()], flush=True)
            print(table, "sample:", db.execute(f"SELECT * FROM nba.{table} LIMIT 1").fetchall(), flush=True)
        except Exception as e:
            print(table, "unavailable:", str(e)[:350], flush=True)
    try:
        players = db.execute("""SELECT DISTINCT p.player_id, x.name
            FROM nba.player_game_logs p JOIN nba.players x ON p.player_id=x.player_id
            WHERE p.season=2027""").fetchall()
        by_name = {}
        for pid, name in players:
            by_name.setdefault(normalize(name), []).append(str(pid))
        matched = [(r.get("player") or r.get("player_name"),r.get("pos"),by_name.get(normalize(r.get("player") or r.get("player_name")),[])) for r in parser.rows]
        print("Exact normalized-name matches:",sum(len(ids)==1 for _,_,ids in matched),"/",len(matched),flush=True)
        print("Unmatched or ambiguous:",[x for x in matched if len(x[2])!=1][:15],flush=True)
        print("Name matches are diagnostic only; do not publish without identity verification.",flush=True)
    except Exception as e:
        print("Player ID bridge query unavailable:",str(e)[:650],flush=True)

if __name__ == "__main__":
    main()
