"""Prioritize blocked team-position cells from the staged seven-player live audit.

Reads the generated complete coverage audit. Does not approve players or
alter the crosswalk, coverage denominators, or publication gates.
"""
import json
from pathlib import Path

SOURCE=Path("reports/2027_staged_seven_player_full_coverage_audit.json")
OUT=Path("reports/2027_staged_seven_player_blocker_priorities.json")
THRESHOLD=.95

def build(report):
    teams=report["teams"];ranked=[]
    for team,stats in teams.items():
        unknown=stats["unknown_rows"];all_rows=stats["all_rows"];known=stats["verified_rows"]
        # Minimum additional VERIFIED rows needed for the team-wide gate.
        team_need=max(0,__import__("math").ceil(THRESHOLD*all_rows-1e-10)-known)
        blocked=[]
        for pos,cell in stats["positions"].items():
            if cell["pass"]:continue
            exact=cell["verified_rows"]
            # Conservative denominator is exact-position rows plus unknown rows.
            # If x previously unknown rows are independently proven to belong to
            # this position, ratio becomes (exact+x)/(exact+unknown).
            required=max(0,__import__("math").ceil(THRESHOLD*(exact+unknown)-exact-1e-10))
            blocked.append({"position":pos,"known_position_rows":exact,
                "unknown_rows_in_conservative_denominator":unknown,
                "minimum_matching_unknown_rows_needed":required,
                "note":"Mathematical lower bound only; not an evidence-based promotion recommendation"})
        if blocked:
            ranked.append({"team":team,"all_rows":all_rows,"verified_rows":known,
                "unknown_rows":unknown,"team_coverage_pct":stats["coverage_pct"],
                "team_gate_pass":stats["team_gate_pass"],
                "minimum_new_verified_rows_for_team_gate":team_need,
                "blocked_position_cells":len(blocked),"positions":blocked})
    ranked.sort(key=lambda t:(-t["blocked_position_cells"],-t["unknown_rows"],t["team"]))
    return {"source":"staged live seven-player coverage audit",
        "leaguewide_coverage_pct":report["leaguewide_coverage_pct"],
        "team_gates_passing":report["team_gates_passing"],
        "position_cells_passing":report["position_cells_passing"],
        "blocked_teams":ranked,"blocked_team_count":len(ranked),
        "blocked_position_cell_count":sum(t["blocked_position_cells"] for t in ranked),
        "publication_ready":False,"crosswalk_modified":False,
        "caution":"Position-cell minimums cannot be summed or used as automatic approvals; same unknown rows affect all five denominators."}

def main():
    report=json.loads(SOURCE.read_text(encoding="utf-8"))
    result=build(report)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("STAGED_SEVEN_BLOCKER_PRIORITIES",json.dumps({
        "blocked_teams":result["blocked_team_count"],
        "blocked_position_cells":result["blocked_position_cell_count"],
        "highest_priority_teams":[x["team"] for x in result["blocked_teams"][:8]],
        "published":False}))

if __name__=="__main__":main()
