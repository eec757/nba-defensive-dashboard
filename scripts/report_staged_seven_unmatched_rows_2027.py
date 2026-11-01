"""Find actual unmatched player-game IDs behind staged seven-player coverage gaps.

Uses the same live source and staged verified crosswalk as the full coverage audit.
Read-only, no inferred player identities or position approvals.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
from publish_verified_positions import CATALOG, TEAM_IDS
from audit_staged_seven_player_full_coverage_2027 import STAGED, REPORT as COVERAGE

OUT=Path("reports/2027_staged_seven_player_unmatched_game_rows_by_team.json")

def main():
    if not STAGED.exists() or not COVERAGE.exists():
        raise ValueError("Run staged seven-player coverage audit first")
    with STAGED.open(newline="",encoding="utf-8") as f:
        verified={r["nba_player_id"] for r in csv.DictReader(f) if r["verified"].lower()=="true"}
    coverage=json.loads(COVERAGE.read_text(encoding="utf-8"))
    import duckdb
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""SELECT p.player_id,p.opp_team_id,p.game_id
      FROM nba.player_game_logs p JOIN nba.games g
        ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'""").fetchall()
    lookup={str(v):k for k,v in TEAM_IDS.items()}
    by_team=defaultdict(lambda:defaultdict(lambda:{"rows":0,"game_ids":[]}))
    for pid,opp,game in rows:
        if str(opp) not in lookup:raise ValueError(f"Unknown opponent team ID: {opp}")
        if str(pid) not in verified:
            entry=by_team[lookup[str(opp)]][str(pid)]
            entry["rows"]+=1;entry["game_ids"].append(str(game))
    total=sum(v["rows"] for team in by_team.values() for v in team.values())
    expected=coverage["all_game_rows"]-coverage["verified_game_rows"]
    if len(rows)!=coverage["all_game_rows"] or total!=expected:
        raise ValueError("Source changed since staged audit; rerun full coverage first")
    teams=[]
    for team,info in coverage["teams"].items():
        unknown=[{"nba_player_id":pid,"unverified_game_rows":v["rows"],
                  "game_ids":sorted(set(v["game_ids"]))}
                 for pid,v in by_team[team].items()]
        unknown.sort(key=lambda v:(-v["unverified_game_rows"],v["nba_player_id"]))
        if len(unknown)==0 and info["unknown_rows"]!=0:
            raise ValueError("Unknown row count mismatch")
        if sum(v["unverified_game_rows"] for v in unknown)!=info["unknown_rows"]:
            raise ValueError("Team unknown row count mismatch")
        teams.append({"team":team,"team_gate_pass":info["team_gate_pass"],
            "blocked_position_cells":sum(not x["pass"] for x in info["positions"].values()),
            "unknown_rows":info["unknown_rows"],"unmatched_player_ids":unknown})
    teams.sort(key=lambda x:(-x["blocked_position_cells"],-x["unknown_rows"],x["team"]))
    result={"source":"live regular-season game logs and staged seven-player crosswalk",
        "all_game_rows":len(rows),"unmatched_rows":total,"teams":teams,
        "identity_evidence_status":"not independently verified by this report",
        "publication_ready":False,"crosswalk_modified":False}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("STAGED_SEVEN_UNMATCHED_ROWS",json.dumps({"unmatched_rows":total,
        "teams_with_unmatched_rows":sum(x["unknown_rows"]>0 for x in teams),
        "highest_priority_teams":[x["team"] for x in teams[:8]],
        "published":False}))

if __name__=="__main__":main()
