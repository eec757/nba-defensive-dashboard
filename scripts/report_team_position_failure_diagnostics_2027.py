"""Detailed, read-only triage of strict 2026-27 team-position coverage failures."""
import json
from collections import Counter
from pathlib import Path

def build():
    scenario=json.loads(Path("reports/missing_player_coverage_scenario_2027.json").read_text(encoding="utf-8"))
    exceptions=json.loads(Path("reports/remaining_game_log_exceptions_2027.json").read_text(encoding="utf-8"))
    players=exceptions["unresolved_players"]
    expected={"1643633","1643568","1643813"}
    actual={p["nba_player_id"] for p in players}
    drift=sorted(actual.symmetric_difference(expected))
    if drift:
        print("TEAM_POSITION_EXCEPTION_SET_DRIFT",json.dumps({"expected":sorted(expected),"actual":sorted(actual),"symmetric_difference":drift,"publication_ready":False}))
    total_unresolved=sum(p["game_rows"] for p in players)
    if total_unresolved<0:
        raise ValueError("Negative unresolved game rows")
    failures=scenario["team_position_gate_failures"]
    rows=[]
    for team,pos in failures:
        relevant=[{"nba_player_id":p["nba_player_id"],
                   "unresolved_rows_against_defending_team":p["defending_teams"][team]}
                  for p in players if team in p["defending_teams"]]
        rows.append({"defending_team":team,"position":pos,
                     "unknown_player_rows_affecting_conservative_denominator":sum(x["unresolved_rows_against_defending_team"] for x in relevant),
                     "unresolved_players":relevant,
                     "failure_class":"conservative_unknown_position_denominator",
                     "exact_coverage_numerator":None,
                     "exact_coverage_denominator":None,
                     "coverage_shortfall":None,
                     "needs_live_position_counts":True,
                     "would_resolve_if_three_positions_verified":"not_established"})
    by_team=dict(sorted(Counter(r["defending_team"] for r in rows).items()))
    return {"scenario":"historical_hypothetical_not_live_coverage",
            "failed_team_position_cells":len(rows),"failed_cells_by_defending_team":by_team,
            "cells":rows,"excluded_game_rows":total_unresolved,
            "exception_set_changed":bool(drift),"expected_exception_ids":sorted(expected),
            "actual_exception_ids":sorted(actual),
            "missing_data":["exact per-cell verified numerator","exact per-cell conservative denominator","latest source refresh"],
            "publication_ready":False,"crosswalk_modified":False,
            "all_coverage_gates_pass":False}

def main():
    report=build()
    out=Path("reports/2027_team_position_failure_diagnostics.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TEAM_POSITION_FAILURE_DIAGNOSTICS",json.dumps({"failed":report["failed_team_position_cells"],"teams":report["failed_cells_by_defending_team"],"publication_ready":False}))

if __name__=="__main__":
    main()
