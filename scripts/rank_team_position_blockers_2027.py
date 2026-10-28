"""Rank historical hypothetical team-position blockers by required verified rows."""
import json
import math
from pathlib import Path
from publish_verified_positions import MIN_COVERAGE

def build():
    report=json.loads(Path("reports/2027_team_position_exact_hypothetical_counts.json").read_text())
    blocked=[]
    for c in report["cells"]:
        if c["passes_95_pct"]:continue
        known=int(c["hypothetical_verified_rows"])
        unknown=int(c["remaining_unknown_rows_for_team"])
        denom=known+unknown
        # Converting x unknown rows to verified rows of THIS position keeps
        # denominator fixed and requires ceil(95%*denom)-known conversions.
        # This is an optimistic bound, not evidence that such rows exist.
        fixed_denominator_needed=max(0,math.ceil(MIN_COVERAGE*denom-1e-12)-known)
        # Unknown rows verified as OTHER positions leave this position's
        # numerator unchanged but shrink its conservative denominator.
        # Need known/(known+unknown-x)>=95%, i.e. x>=unknown-known*(1/.95-1).
        other_position_needed=max(0,math.ceil(unknown-known*(1/MIN_COVERAGE-1)-1e-12)) if known else None
        blocked.append({**c,"minimum_same_position_conversions_fixed_denominator":fixed_denominator_needed,
                        "minimum_other_position_resolutions":other_position_needed,
                        "unknown_rows_available":unknown,
                        "can_pass_via_same_position_conversion_within_unknown_pool":fixed_denominator_needed<=unknown,
                        "not_a_recommendation_to_infer_position":True})
    blocked.sort(key=lambda c:(c["minimum_same_position_conversions_fixed_denominator"],c["team"],c["position"]))
    if len(blocked)!=report["failed_cells"]:
        raise ValueError("Ranking does not reconcile to failed cells")
    return {"basis":"historical hypothetical counts, not live coverage",
            "ranked_blockers":blocked,"blocked_count":len(blocked),
            "publication_ready":False,"crosswalk_modified":False}

def main():
    result=build()
    out=Path("reports/2027_ranked_team_position_blockers.json")
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("RANKED_TEAM_POSITION_BLOCKERS",json.dumps({"blocked":len(result["ranked_blockers"]),
        "smallest_required_conversions":result["ranked_blockers"][0]["minimum_same_position_conversions_fixed_denominator"] if result["ranked_blockers"] else 0,
        "publication_ready":False}))

if __name__=="__main__":main()
