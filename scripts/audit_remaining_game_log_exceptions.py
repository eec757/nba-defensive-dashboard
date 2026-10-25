"""Report the exact game-level blockers after the seven-player evidence scenario.

Read-only. No guessed identities, positions, approvals, or publication.
"""
import json
from pathlib import Path

def main():
    unmatched=json.loads(Path("reports/unmatched_player_games_2027.json").read_text())
    evidence=json.loads(Path("reports/missing_player_position_evidence_2027.json").read_text())
    scenario=json.loads(Path("reports/missing_player_coverage_scenario_2027.json").read_text())
    by_id={p["nba_player_id"]:p for p in evidence["players"]}
    unresolved=[]
    for player in unmatched["players"]:
        match=by_id[player["nba_player_id"]]
        if match["season_position_verified"]:continue
        candidates=match["identity_candidates"]
        unresolved.append({
            "nba_player_id":player["nba_player_id"],
            "game_rows":player["game_rows"],
            "defending_teams":player["defending_teams"],
            "game_ids":player["game_ids"],
            "identity_candidates":candidates,
            "needs_exact_bref_id":not (len(candidates)==1 and bool(candidates[0]["bref_id"])),
            "needs_season_roster_position":not match["season_position_verified"],
            "human_approved":False
        })
    result={"unresolved_players":unresolved,
            "unresolved_game_rows":sum(p["game_rows"] for p in unresolved),
            "remaining_team_position_failures":scenario["team_position_gate_failures"],
            "publication_ready":False,
            "next_action":"Independently verify exact identities and 2026-27 positions; no inferred assignments."}
    if result["unresolved_game_rows"]!=scenario["remaining_unknown_rows"]:
        raise ValueError("Mismatch between scenario and unresolved player-game counts")
    out=Path("reports/remaining_game_log_exceptions_2027.json")
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("REMAINING_GAME_LOG_EXCEPTIONS",json.dumps(result))

if __name__=="__main__":main()
