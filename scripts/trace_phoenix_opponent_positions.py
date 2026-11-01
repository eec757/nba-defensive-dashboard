"""Read-only row-level trace of opponent game logs defended by Phoenix."""
import csv
import json
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG, TEAM_IDS

OUT = Path("reports/2027_phoenix_opponent_position_trace.csv")
SUMMARY = Path("reports/2027_phoenix_opponent_position_trace.json")

def main():
    with Path("reports/proposed_verified_player_ids_2027.csv").open(newline="", encoding="utf-8") as f:
        proposal = list(csv.DictReader(f))
    with Path("reports/season_position_evidence_2027.csv").open(newline="", encoding="utf-8") as f:
        evidence = list(csv.DictReader(f))
    supported = {(r["nba_player_id"], r["bref_id"]) for r in evidence if r["status"] == "supported"}
    verified = {r["nba_player_id"]: r for r in proposal if (r["nba_player_id"], r["bref_id"]) in supported}
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows = db.execute("""
        SELECT CAST(p.player_id AS VARCHAR), CAST(p.game_id AS VARCHAR),
               CAST(p.opp_team_id AS VARCHAR)
        FROM nba.player_game_logs p JOIN nba.games g
          ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
          AND p.opp_team_id=?
        ORDER BY p.game_id, p.player_id
    """, [int(TEAM_IDS["PHO"])]).fetchall()
    if not rows:
        raise ValueError("No Phoenix-defended opponent game logs; refusing empty trace")
    output = []
    for pid, game, defending_id in rows:
        matched = verified.get(pid)
        output.append({"game_id":game,"defending_team":"PHO",
                       "defending_team_id":defending_id,"opponent_nba_player_id":pid,
                       "verified_bref_id":matched["bref_id"] if matched else "",
                       "verified_position":matched["position"] if matched else "",
                       "position_status":"season_supported_proposal" if matched else "unmatched",
                       "published":"false"})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(output[0]));writer.writeheader();writer.writerows(output)
    counts={pos:sum(r["verified_position"]==pos for r in output) for pos in ("PG","SG","SF","PF","C")}
    summary={"defending_team":"PHO","opponent_game_rows":len(output),
             "verified_position_rows":counts,
             "unmatched_rows":sum(r["position_status"]=="unmatched" for r in output),
             "distinct_game_ids":sorted({r["game_id"] for r in output}),
             "publication_ready":False,"crosswalk_modified":False,
             "note":"PHO opponent observations only; PHO roster guards cannot supply opponent SG rows."}
    SUMMARY.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print("PHOENIX_OPPONENT_POSITION_TRACE",json.dumps(summary))

if __name__=="__main__":main()
