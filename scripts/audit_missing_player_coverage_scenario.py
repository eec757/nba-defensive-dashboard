"""Read-only what-if coverage for seven evidence-supported, unapproved players."""
import json
from pathlib import Path
from publish_verified_positions import POSITIONS,MIN_COVERAGE

def main():
    base=json.loads(Path("reports/proposed_game_coverage_2027.json").read_text())
    missing=json.loads(Path("reports/missing_player_position_evidence_2027.json").read_text())
    teams=base["teams"]
    additions={t:{p:0 for p in POSITIONS} for t in teams}
    by_id={p["nba_player_id"]:p for p in missing["players"]}
    unmatched=json.loads(Path("reports/unmatched_player_games_2027.json").read_text())
    for player in unmatched["players"]:
        candidate=by_id[player["nba_player_id"]]
        if not candidate["season_position_verified"]:continue
        evidence=candidate["season_position_evidence"]
        positions={x["position"] for x in evidence}
        if len(positions)!=1:continue
        pos=next(iter(positions))
        for team,n in player["defending_teams"].items():
            additions[team][pos]+=n
    failures_team=[]
    failures_position=[]
    remaining=0
    for team,c in teams.items():
        gained=sum(additions[team].values())
        unknown=c["unknown_rows"]-gained
        if unknown<0:raise ValueError("Scenario exceeds unknown game rows")
        remaining+=unknown
        known=c["verified_rows"]+gained
        if not c["all_player_game_rows"] or known/c["all_player_game_rows"]<MIN_COVERAGE:
            failures_team.append(team)
        for pos in POSITIONS:
            verified=c["positions"][pos]["verified_rows"]+additions[team][pos]
            denom=verified+unknown
            if not verified or not denom or verified/denom<MIN_COVERAGE:
                failures_position.append([team,pos])
    total=base["total_game_rows"]
    result={"scenario":"Seven season-supported game-log identities added hypothetically; no approvals",
            "total_game_rows":total,"hypothetical_covered_rows":total-remaining,
            "hypothetical_leaguewide_coverage_pct":round(100*(total-remaining)/total,2),
            "remaining_unknown_rows":remaining,"team_gate_failures":failures_team,
            "team_position_gate_failures":failures_position,
            "all_coverage_gates_pass":not failures_team and not failures_position and (total-remaining)/total>=MIN_COVERAGE,
            "publication_ready":False,"crosswalk_modified":False}
    Path("reports/missing_player_coverage_scenario_2027.json").write_text(json.dumps(result,indent=2)+"\\n")
    print("MISSING_PLAYER_COVERAGE_SCENARIO",json.dumps(result))

if __name__=="__main__":main()
