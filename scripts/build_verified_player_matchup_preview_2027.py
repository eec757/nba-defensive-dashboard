"""Build a non-published individual matchup game-log preview.

Only explicitly verified IDs are included. Preview is an audit artifact, not a
public dashboard feed; position-defense publication gates remain unchanged.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG

CROSSWALK=Path("data/verified_player_ids_2027.csv")
OUT=Path("reports/2027_verified_player_matchup_game_log_preview.json")
def main():
    with CROSSWALK.open(newline="",encoding="utf-8") as f:
        verified={str(r["nba_player_id"]).strip():r["position"].strip()
            for r in csv.DictReader(f) if r.get("verified","").strip().lower()=="true"
            and r.get("position","").strip() in ("PG","SG","SF","PF","C")}
    if not verified:raise ValueError("No explicitly verified player IDs")
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""
        SELECT CAST(p.player_id AS VARCHAR),CAST(p.opp_team_id AS VARCHAR),
               CAST(p.game_id AS VARCHAR),p.pts,p.reb,p.ast,p.fgm,p.fga,p.fg3m,p.fg3a
        FROM nba.player_game_logs p
        JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    stats=defaultdict(lambda:{"games":set(),"pts":0,"reb":0,"ast":0,"fgm":0,"fga":0,"three_pm":0,"three_pa":0})
    for pid,opp,gid,pts,reb,ast,fgm,fga,three_pm,three_pa in rows:
        if pid not in verified:continue
        s=stats[pid]
        if gid in s["games"]:raise ValueError("Duplicate verified player-game row")
        s["games"].add(gid)
        for key,value in (("pts",pts),("reb",reb),("ast",ast),("fgm",fgm),("fga",fga),("three_pm",three_pm),("three_pa",three_pa)):
            s[key]+=float(value or 0)
    players=[]
    for pid in sorted(stats):
        s=stats[pid];n=len(s["games"])
        players.append({"nba_player_id":pid,"verified_position":verified[pid],"games":n,
            "points_per_game":round(s["pts"]/n,2),"rebounds_per_game":round(s["reb"]/n,2),
            "assists_per_game":round(s["ast"]/n,2),"threes_made_per_game":round(s["three_pm"]/n,2),
            "threes_attempted_per_game":round(s["three_pa"]/n,2),
            "fg_pct":round(100*s["fgm"]/s["fga"],1) if s["fga"] else None,
            "three_pct":round(100*s["three_pm"]/s["three_pa"],1) if s["three_pa"] else None})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({"season":"2026-27","source":CATALOG,
        "verified_players_in_logs":len(players),"total_player_game_rows":len(rows),
        "published":False,"production_modified":False,
        "note":"Review-only preview. No per-player minimum games or leaguewide coverage publication gate has been applied.",
        "players":players},indent=2)+"\n",encoding="utf-8")
    print("VERIFIED_PLAYER_MATCHUP_PREVIEW",json.dumps({"verified_players_in_logs":len(players),
        "total_player_game_rows":len(rows),"published":False}))
if __name__=="__main__":main()
