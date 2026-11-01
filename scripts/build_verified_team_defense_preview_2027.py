"""Read-only team-level defensive analytics preview, independent of exact positions.

Only rows with independently verified crosswalk identities contribute to totals.
All raw rows (including UNKNOWN positions) remain in coverage denominators.
No production JSON is written; 95% leaguewide and per-team gates are unchanged.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
from publish_verified_positions import CROSSWALK, TEAM_IDS, MIN_COVERAGE, CATALOG, validate_crosswalk_source, validate_independent_evidence

OUT=Path("reports/2027_verified_team_defense_preview.json")

def calculate_team_preview(rows, verified_ids, team_ids=TEAM_IDS):
    lookup={str(v):k for k,v in team_ids.items()}
    stats=defaultdict(lambda:{"all_rows":0,"verified_rows":0,"games":set(),"pts":0.0,"reb":0.0,"ast":0.0})
    total=covered=0
    for pid,opp,game,pts,reb,ast in rows:
        team=lookup.get(str(opp))
        if team is None:raise ValueError(f"Unrecognized opponent team ID: {opp}")
        s=stats[team];s["all_rows"]+=1;s["games"].add(str(game));total+=1
        if str(pid) not in verified_ids:continue
        s["verified_rows"]+=1;covered+=1
        s["pts"]+=float(pts or 0);s["reb"]+=float(reb or 0);s["ast"]+=float(ast or 0)
    if not total:raise ValueError("No player-game rows")
    league_ok=covered/total>=MIN_COVERAGE
    result={}
    for team in team_ids:
        s=stats[team];n=len(s["games"])
        coverage=s["verified_rows"]/s["all_rows"] if s["all_rows"] else 0
        ready=bool(league_ok and n and coverage>=MIN_COVERAGE)
        result[team]={"all_player_game_rows":s["all_rows"],"verified_player_game_rows":s["verified_rows"],
                      "unknown_player_game_rows":s["all_rows"]-s["verified_rows"],
                      "team_coverage_pct":round(100*coverage,3),"defending_games":n,
                      "meets_team_and_leaguewide_95_pct":ready,
                      "verified_only_metrics":({"points_allowed_per_game":round(s["pts"]/n,2),
                                                "rebounds_allowed_per_game":round(s["reb"]/n,2),
                                                "assists_allowed_per_game":round(s["ast"]/n,2)}
                                               if ready else None)}
    return {"leaguewide_covered_rows":covered,"leaguewide_all_rows":total,
            "leaguewide_coverage_pct":round(100*covered/total,3),
            "leaguewide_gate_pass":league_ok,"teams":result,
            "published":False,"production_output_modified":False,
            "position_gate_bypassed":False,"note":"Separate team-only preview, not position-defense publication. Metrics exclude unknown rows; coverage denominator includes them."}

def main():
    with CROSSWALK.open(newline="",encoding="utf-8") as f:records=list(csv.DictReader(f))
    verified=set()
    for r in records:
        if r["verified"].strip().lower()!="true":continue
        validate_crosswalk_source(r["verification_source"])
        validate_independent_evidence(r)
        if r["nba_player_id"] in verified:raise ValueError("Duplicate verified NBA ID")
        verified.add(r["nba_player_id"])
    if not verified:raise ValueError("No verified identities; fail closed")
    import duckdb
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""SELECT p.player_id,p.opp_team_id,p.game_id,p.pts,p.reb,p.ast
      FROM nba.player_game_logs p JOIN nba.games g
      ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'""").fetchall()
    report=calculate_team_preview(rows,verified)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("VERIFIED_TEAM_DEFENSE_PREVIEW",json.dumps({"leaguewide_coverage_pct":report["leaguewide_coverage_pct"],
        "leaguewide_gate_pass":report["leaguewide_gate_pass"],
        "team_gates_passing":sum(v["meets_team_and_leaguewide_95_pct"] for v in report["teams"].values()),
        "published":False}))

if __name__=="__main__":main()
