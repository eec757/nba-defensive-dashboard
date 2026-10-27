"""Summarize strict hypothetical team-position blockers without changing gates."""
import json
from pathlib import Path

scenario=json.loads(Path("reports/missing_player_coverage_scenario_2027.json").read_text())
unresolved=json.loads(Path("reports/remaining_game_log_exceptions_2027.json").read_text())
from display_exclusions_2027 import EXCLUDED_PLAYER_IDS
excluded={"1643633":"Graham Ike","1643568":"Nick Martinelli","1643813":"Alpha Diallo"}
if set(excluded) != EXCLUDED_PLAYER_IDS:
    raise ValueError("Blocker report and display exclusion IDs have drifted")
players=unresolved.get("unresolved_players",[])
actual_unknown=sum(p["game_rows"] for p in players)
if actual_unknown != scenario["remaining_unknown_rows"]:
    raise ValueError("Unresolved rows do not match scenario denominator")
if {p["nba_player_id"] for p in players} != EXCLUDED_PLAYER_IDS:
    raise ValueError("Unresolved player set changed; manual review required")
failures=scenario["team_position_gate_failures"]
rows=[]
for team,position in failures:
    affected=[{"nba_player_id":p["nba_player_id"],"name":excluded[p["nba_player_id"]],
               "game_rows_for_team":p["defending_teams"][team]}
              for p in players if p["nba_player_id"] in excluded and team in p["defending_teams"]]
    rows.append({"defending_team":team,"position":position,
                 "excluded_unresolved_players":affected,
                 "reason":"conservative_unknown_rows_in_denominator",
                 "verified_position_specific_coverage":"not_established_by_this_report"})
report={"scenario":"hypothetical_only_not_publication_approval",
        "team_position_gate_failures":len(rows),"blocked_team_positions":rows,
        "excluded_player_ids":sorted(excluded),"unresolved_game_rows":scenario["remaining_unknown_rows"],
        "all_coverage_gates_pass":scenario["all_coverage_gates_pass"],
        "publication_ready":False,
        "note":"An unresolved player may affect every position's conservative denominator for a defending team; this does not imply they played all positions. Actual approved coverage remains separate."}
out=Path("reports/2027_team_position_blocker_summary.json")
out.write_text(json.dumps(report,indent=2)+"\n")
print("TEAM_POSITION_BLOCKER_SUMMARY",json.dumps({"failed":len(rows),"teams":sorted({r["defending_team"] for r in rows}),"excluded_players":len(excluded),"publication_ready":False}))
