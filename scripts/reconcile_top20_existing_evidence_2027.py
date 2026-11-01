"""Reconcile top-20 unmatched IDs with existing independently supported evidence.

Evidence-only report; no player is approved, staged, or signed off.
"""
import csv
import json
from pathlib import Path

ROOT=Path("reports")
IN=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
OUT=ROOT/"2027_top20_existing_evidence_reconciliation.json"

def read_csv(path):
    if not path.exists():return []
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def main():
    queue=json.loads(IN.read_text(encoding="utf-8"))["priority_players"][:20]
    proposed=read_csv(ROOT/"proposed_verified_player_ids_2027.csv")
    season=read_csv(ROOT/"season_position_evidence_2027.csv")
    supported={(r.get("nba_player_id"),r.get("bref_id")):r for r in season if r.get("status")=="supported"}
    by_id={}
    for r in proposed:by_id.setdefault(r.get("nba_player_id"),[]).append(r)
    results=[]
    for player in queue:
        pid=player["nba_player_id"]
        candidates=[]
        for r in by_id.get(pid,[]):
            evidence=supported.get((pid,r.get("bref_id")))
            candidates.append({"candidate_bref_id":r.get("bref_id"),
                "candidate_position":r.get("position"),
                "season_position_supported":evidence is not None,
                "season_evidence_position":evidence.get("position") if evidence else None,
                "independent_dual_id_verified":False,
                "owner_approval":False})
        results.append({"nba_player_id":pid,
            "unmatched_game_rows":player["unmatched_game_rows"],
            "affected_teams":player["affected_teams"],
            "existing_candidate_rows":candidates,
            "review_status":"independent_dual_id_and_exact_position_evidence_required",
            "promotable":False})
    report={"scope":"top 20 unmatched player IDs",
        "players_reviewed":len(results),
        "players_with_existing_candidates":sum(bool(r["existing_candidate_rows"]) for r in results),
        "players_with_season_supported_candidate":sum(any(c["season_position_supported"] for c in r["existing_candidate_rows"]) for r in results),
        "players_approved":0,"crosswalk_modified":False,"publication_ready":False,
        "players":results}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_EXISTING_EVIDENCE_RECONCILIATION",json.dumps({
        k:report[k] for k in ("players_reviewed","players_with_existing_candidates",
        "players_with_season_supported_candidate","players_approved","publication_ready")}))

if __name__=="__main__":main()
