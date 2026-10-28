"""Reconstruct exact hypothetical per-cell position coverage from audit inputs.

Strictly a what-if report: approved crosswalk and publication gates are untouched.
"""
import json
import csv
from pathlib import Path
from publish_verified_positions import POSITIONS,MIN_COVERAGE

def build():
    base=json.loads(Path("reports/proposed_game_coverage_2027.json").read_text())
    missing=json.loads(Path("reports/missing_player_position_evidence_2027.json").read_text())
    unmatched=json.loads(Path("reports/unmatched_player_games_2027.json").read_text())
    scenario=json.loads(Path("reports/missing_player_coverage_scenario_2027.json").read_text())
    with Path("reports/proposed_verified_player_ids_2027.csv").open(newline="",encoding="utf-8") as f:
        proposed=list(csv.DictReader(f))
    with Path("reports/season_position_evidence_2027.csv").open(newline="",encoding="utf-8") as f:
        evidence=list(csv.DictReader(f))
    supported={(r["nba_player_id"],r["bref_id"]) for r in evidence if r["status"]=="supported"}
    baseline_ids={r["nba_player_id"] for r in proposed if (r["nba_player_id"],r["bref_id"]) in supported}
    by_id={p["nba_player_id"]:p for p in missing["players"]}
    additions={team:{p:0 for p in POSITIONS} for team in base["teams"]}
    for p in unmatched["players"]:
        pid=p["nba_player_id"]
        if pid in baseline_ids:continue
        candidate=by_id[pid]
        if not candidate["season_position_verified"]:continue
        positions={x["position"] for x in candidate["season_position_evidence"]}
        if len(positions)!=1 or next(iter(positions)) not in POSITIONS:continue
        position=next(iter(positions))
        for team,n in p["defending_teams"].items():
            additions[team][position]+=n
    rows=[]
    failed=[]
    for team,c in base["teams"].items():
        gained=sum(additions[team].values())
        unknown=c["unknown_rows"]-gained
        if unknown<0:raise ValueError("Negative unknown rows")
        for pos in POSITIONS:
            verified=c["positions"][pos]["verified_rows"]+additions[team][pos]
            denominator=verified+unknown
            pct=100*verified/denominator if denominator else 0
            passes=bool(verified and denominator and verified/denominator>=MIN_COVERAGE)
            if not passes:failed.append([team,pos])
            rows.append({"team":team,"position":pos,"hypothetical_verified_rows":verified,
                         "remaining_unknown_rows_for_team":unknown,
                         "conservative_denominator":denominator,"coverage_pct":round(pct,4),
                         "passes_95_pct":passes,"baseline_position_rows":c["positions"][pos]["verified_rows"],
                         "hypothetical_added_position_rows":additions[team][pos]})
    if sorted(failed)!=sorted(scenario["team_position_gate_failures"]):
        raise ValueError("Reconstructed failed cells differ from existing scenario")
    return {"basis":"reconstruction of existing historical hypothetical scenario, not live approved coverage",
            "cells":rows,"failed_cells":len(failed),"publication_ready":False,
            "crosswalk_modified":False,"all_coverage_gates_pass":False}

def main():
    report=build()
    path=Path("reports/2027_team_position_exact_hypothetical_counts.json")
    path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TEAM_POSITION_EXACT_HYPOTHETICAL_COUNTS",json.dumps({"cells":len(report["cells"]),"failed":report["failed_cells"],"scenario_reconciled":True,"publication_ready":False}))

if __name__=="__main__":main()
