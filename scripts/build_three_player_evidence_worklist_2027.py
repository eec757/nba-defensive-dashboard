"""Produce a prioritized, non-approving evidence worklist for three excluded players."""
import json
from pathlib import Path

SOURCE=Path("reports/remaining_game_log_exceptions_2027.json")
OUTPUT=Path("reports/2027_three_player_evidence_worklist.json")
NAMES={"1643633":"Graham Ike","1643568":"Nick Martinelli","1643813":"Alpha Diallo"}
EXPECTED={"1643633":4,"1643568":1,"1643813":1}

def main():
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    players={p["nba_player_id"]:p for p in data["unresolved_players"]}
    if set(players)!=set(NAMES):raise ValueError("Excluded player set changed")
    if {pid:players[pid]["game_rows"] for pid in players}!=EXPECTED:
        raise ValueError("Excluded player-game counts changed; refresh audit")
    work=[]
    for pid in sorted(players,key=lambda x:-players[x]["game_rows"]):
        p=players[pid]
        work.append({
            "nba_player_id":pid,"name":NAMES[pid],"affected_game_rows":p["game_rows"],
            "defending_teams":p["defending_teams"],"game_ids":p["game_ids"],
            "exact_bref_link_required":pid=="1643813",
            "season_2026_27_primary_position_evidence_required":True,
            "evidence_tasks":([
                "Find an independent source linking exact NBA numeric ID to exact Basketball Reference ID"
            ] if pid=="1643813" else [])+[
                "Verify the player's 2026-27 season-specific primary position from the exact roster row",
                "Reconcile source discrepancies and record the supporting URL and observed row",
                "Obtain explicit attributable human approval only after evidence review"
            ],
            "approved":False,"included_in_publication":False
        })
    result={"players":work,"excluded_game_rows":sum(x["affected_game_rows"] for x in work),
            "publication_ready":False,"coverage_denominator_preserved":True}
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("THREE_PLAYER_EVIDENCE_WORKLIST",json.dumps({"players":len(work),"excluded_game_rows":result["excluded_game_rows"],"publication_ready":False}))

if __name__=="__main__":main()
