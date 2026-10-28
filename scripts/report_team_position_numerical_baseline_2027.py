"""Read-only numerical baseline for team-position blockers.

Reports audited proposed baseline numerators and conservative denominators.
Never labels hypothetical proposal counts as approved/current publication coverage.
"""
import json
from pathlib import Path
from publish_verified_positions import POSITIONS, MIN_COVERAGE

def build():
    base=json.loads(Path("reports/proposed_game_coverage_2027.json").read_text())
    scenario=json.loads(Path("reports/missing_player_coverage_scenario_2027.json").read_text())
    failures={tuple(x) for x in scenario["team_position_gate_failures"]}
    rows=[]
    for team,pos in sorted(failures):
        c=base["teams"][team]
        verified=int(c["positions"][pos]["verified_rows"])
        unknown=int(c["unknown_rows"])
        denom=verified+unknown
        ratio=verified/denom if denom else 0
        required=max(0, __import__("math").ceil(MIN_COVERAGE*denom-1e-12)-verified)
        rows.append({"team":team,"position":pos,"baseline_verified_position_rows":verified,
                     "baseline_unknown_team_rows":unknown,"baseline_conservative_denominator":denom,
                     "baseline_conservative_coverage_pct":round(100*ratio,3),
                     "baseline_rows_short_of_95_pct_at_fixed_denominator":required,
                     "scenario_unknown_rows_after_hypothetical_additions":None,
                     "scenario_exact_position_numerator":None,
                     "scenario_exact_denominator":None,
                     "scenario_failure_confirmed":True,
                     "note":"Baseline is a proposed/hypothetical roster; scenario additions not reconstructed here."})
    return {"basis":"proposed_game_coverage_2027.json baseline; not live published or approved coverage",
            "scenario_failed_cells":len(rows),"cells":rows,
            "scenario_exact_counts_available":False,
            "publication_ready":False,"crosswalk_modified":False}

def main():
    result=build()
    out=Path("reports/2027_team_position_numerical_baseline.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("TEAM_POSITION_NUMERICAL_BASELINE",json.dumps({"failed_cells":len(result["cells"]),"basis":"proposed baseline","scenario_exact_counts_available":False,"publication_ready":False}))

if __name__=="__main__":main()
