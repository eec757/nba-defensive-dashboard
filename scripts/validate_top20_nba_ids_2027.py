"""Validate top-20 NBA IDs against nba_api's bundled official-ID lookup.

NBA ID/name checks are NOT NBA-to-BRef crosswalk verification. This diagnostic
never promotes candidates or treats name similarity as independent evidence.
"""
import csv
import json
from pathlib import Path

ROOT=Path("reports")
QUEUE=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
CANDIDATES=ROOT/"proposed_verified_player_ids_2027.csv"
OUT=ROOT/"2027_top20_nba_id_identity_checks.json"

def main():
    from nba_api.stats.static import players
    queue=json.loads(QUEUE.read_text(encoding="utf-8"))["priority_players"][:20]
    with CANDIDATES.open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    by_id={}
    for r in rows:by_id.setdefault(str(r.get("nba_player_id","")),[]).append(r)
    results=[]
    for q in queue:
        pid=str(q["nba_player_id"])
        player=players.find_player_by_id(int(pid))
        candidates=by_id.get(pid,[])
        results.append({"nba_player_id":pid,
            "nba_api_player_name":player["full_name"] if player else None,
            "nba_id_present_in_nba_api_static":player is not None,
            "candidate_bref_ids":sorted({r.get("bref_id","") for r in candidates if r.get("bref_id")}),
            "candidate_positions":sorted({r.get("position","") for r in candidates if r.get("position")}),
            "nba_bref_crosswalk_independently_verified":False,
            "exact_2026_27_position_verified":False,
            "approved":False,
            "review_status":"dual_id_and_exact_season_position_evidence_required"})
    report={"source":"nba_api.stats.static.players.find_player_by_id",
        "source_kind":"bundled offline lookup, not independent dual-ID evidence",
        "players_checked":len(results),
        "nba_ids_found":sum(r["nba_id_present_in_nba_api_static"] for r in results),
        "nba_ids_not_found":sum(not r["nba_id_present_in_nba_api_static"] for r in results),
        "independently_verified_crosswalks":0,"new_approvals":0,
        "crosswalk_modified":False,"published":False,"players":results}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_NBA_IDENTITY_CHECKS",json.dumps({
        k:report[k] for k in ("players_checked","nba_ids_found","nba_ids_not_found","independently_verified_crosswalks","new_approvals","published")}))

if __name__=="__main__":main()
