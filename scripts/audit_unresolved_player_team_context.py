"""Read-only investigation of unresolved players' actual game-log team affiliations."""
import json
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG,TEAM_IDS

def main():
    report=json.loads(Path("reports/remaining_game_log_exceptions_2027.json").read_text())
    ids=[p["nba_player_id"] for p in report["unresolved_players"]]
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    cols={row[0] for row in db.execute("DESCRIBE SELECT * FROM nba.player_game_logs").fetchall()}
    team_col=next((c for c in ("team_id","player_team_id") if c in cols),None)
    result={"team_column":team_col,"players":[],"published":False}
    lookup={str(v):k for k,v in TEAM_IDS.items()}
    for pid in ids:
        player=next(p for p in report["unresolved_players"] if p["nba_player_id"]==pid)
        if team_col:
            rows=db.execute(f"""SELECT DISTINCT p.{team_col},p.game_id
                FROM nba.player_game_logs p JOIN nba.games g
                ON p.season=g.season AND p.game_id=g.game_id
                WHERE p.season=2027 AND g.game_type='regular_season'
                AND CAST(p.player_id AS VARCHAR)=?""",[pid]).fetchall()
            games=[{"game_id":str(gid),"player_team":lookup.get(str(tid),"unknown")}
                   for tid,gid in rows]
        else:
            games=[]
        result["players"].append({"nba_player_id":pid,"game_teams":games,
            "season_position_verified":False,"human_approved":False,
            "note":"Game-log team membership is not evidence of position."})
    result["review_targets"]=[]
    for player in result["players"]:
        teams=sorted({g["player_team"] for g in player["game_teams"] if g["player_team"]!="unknown"})
        result["review_targets"].append({
            "nba_player_id":player["nba_player_id"],
            "player_team_roster_urls":[f"https://www.basketball-reference.com/teams/{t}/2027.html" for t in teams],
            "needs_independent_identity_and_position_review":True})
    Path("reports/unresolved_player_team_context_2027.json").write_text(json.dumps(result,indent=2)+"\n")
    print("UNRESOLVED_PLAYER_TEAM_CONTEXT",json.dumps(result))

if __name__=="__main__":main()
