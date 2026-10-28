"""Read-only UNKNOWN position bucket for the three unresolved 2026-27 players.

UNKNOWN is a diagnostic label, never a verified PG/SG/SF/PF/C role.
No crosswalk, production output, or publication gate is changed.
"""
import json
from pathlib import Path

EXCEPTIONS={
    "1643633":{"name":"Graham Ike","candidate_position":"PF","game_rows":4,"identity_status":"candidate","reason":"2026-27 roster uses broad F"},
    "1643568":{"name":"Nick Martinelli","candidate_position":"SF","game_rows":1,"identity_status":"candidate","reason":"2026-27 roster uses broad F"},
    "1643813":{"name":"Alpha Diallo","candidate_position":"SG","game_rows":1,"identity_status":"independent_exact_link_pending","reason":"2026-27 roster uses broad G; cross-provider identity link pending"},
}

def build_unknown_report():
    from display_exclusions_2027 import EXCLUDED_PLAYER_IDS
    if set(EXCEPTIONS)!=EXCLUDED_PLAYER_IDS:
        raise ValueError("UNKNOWN roster and excluded IDs drifted")
    players=[{"nba_player_id":pid,"position":"UNKNOWN","eligible_for_exact_position_stats":False,
              "eligible_for_verified_coverage":False,"eligible_for_team_stats":False,
              "team_stats_pending_independent_identity_review":True,**info}
             for pid,info in EXCEPTIONS.items()]
    assert sum(p["game_rows"] for p in players)==6
    return {"season":"2026-27","category":"UNKNOWN","scope":"diagnostic_only",
            "players":players,"unresolved_game_rows_in_coverage_denominator":6,
            "excluded_from_exact_position_metrics":True,
            "verified_crosswalk_modified":False,"publication_gates_unchanged":True,
            "publication_ready":False}

def main():
    out=Path("reports/2027_unknown_position_diagnostics.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    report=build_unknown_report()
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("UNKNOWN_POSITION_DIAGNOSTICS",json.dumps({"players":3,"unknown_rows":6,"publication_ready":False}))

if __name__=="__main__":
    main()
