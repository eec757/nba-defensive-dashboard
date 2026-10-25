"""Measure real game-log coverage from proposed, season-supported identities.

Read-only: this script never promotes approvals or publishes dashboard data.
A position's conservative coverage treats every unknown opponent row as potentially
belonging to that position, avoiding inflated completeness estimates.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG, TEAM_IDS, POSITIONS, MIN_COVERAGE

def main():
    with Path("reports/proposed_verified_player_ids_2027.csv").open(newline="",encoding="utf-8") as f:
        proposal=list(csv.DictReader(f))
    with Path("reports/season_position_evidence_2027.csv").open(newline="",encoding="utf-8") as f:
        evidence=list(csv.DictReader(f))
    supported={(r["nba_player_id"],r["bref_id"]) for r in evidence if r["status"]=="supported"}
    verified={r["nba_player_id"]:r["position"] for r in proposal
              if (r["nba_player_id"],r["bref_id"]) in supported and r["verified"].lower()=="true"}
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""
      SELECT p.player_id,p.opp_team_id,p.game_id
      FROM nba.player_game_logs p JOIN nba.games g
      ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    teams={str(v):k for k,v in TEAM_IDS.items()}
    counts=defaultdict(lambda:{"all":0,"verified":0,"unknown":0,"positions":defaultdict(int)})
    for pid,opp,game in rows:
        team=teams.get(str(opp))
        if not team:
            raise ValueError(f"Unknown defending team: {opp}")
        c=counts[team]
        c["all"]+=1
        pos=verified.get(str(pid))
        if pos:
            c["verified"]+=1
            c["positions"][pos]+=1
        else:
            c["unknown"]+=1
    total=len(rows)
    matched=sum(c["verified"] for c in counts.values())
    team_report={}
    all_pass=bool(total) and matched/total>=MIN_COVERAGE
    for team in TEAM_IDS:
        c=counts[team]
        n=c["all"]
        team_rate=c["verified"]/n if n else 0
        position_report={}
        for pos in POSITIONS:
            count=c["positions"][pos]
            # All unknown player-games could have this position.
            denominator=count+c["unknown"]
            conservative=count/denominator if denominator else 0
            position_report[pos]={"verified_rows":count,"potential_unknown_rows":c["unknown"],
                "conservative_coverage_pct":round(100*conservative,2),
                "passes_95_pct":bool(count) and conservative>=MIN_COVERAGE}
        team_pass=bool(n) and team_rate>=MIN_COVERAGE
        all_pass=all_pass and team_pass and all(x["passes_95_pct"] for x in position_report.values())
        team_report[team]={"all_player_game_rows":n,"verified_rows":c["verified"],
            "unknown_rows":c["unknown"],"coverage_pct":round(100*team_rate,2),
            "passes_95_pct":team_pass,"positions":position_report}
    report={"total_game_rows":total,"verified_game_rows":matched,
        "leaguewide_coverage_pct":round(100*matched/total,2) if total else 0,
        "minimum_required_pct":100*MIN_COVERAGE,"teams":team_report,
        "all_coverage_gates_pass":bool(all_pass),
        "publication_ready":False,
        "note":"Read-only proposal coverage; passing is not approval or publication. Conservative per-position denominator includes every unknown player-game."}
    out=Path("reports/proposed_game_coverage_2027.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("PROPOSED_GAME_COVERAGE",json.dumps({k:v for k,v in report.items() if k!="teams"}))
    print("TEAM_COVERAGE_FAILURES",json.dumps([t for t,c in team_report.items() if not c["passes_95_pct"]]))
    print("POSITION_COVERAGE_FAILURES",json.dumps([(t,p) for t,c in team_report.items() for p,x in c["positions"].items() if not x["passes_95_pct"]]))

if __name__=="__main__":
    main()
