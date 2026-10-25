"""Stage Wikidata NBA-ID evidence for game-log players missing from roster queue.

Read-only. No identity is approved without exact BRef ID, independent evidence,
season-specific roster position, and explicit review.
"""
import json
import time
from pathlib import Path
import requests
from stage_wikidata_exact_evidence import query_wikidata

INPUT=Path("reports/unmatched_player_games_2027.json")
OUTPUT=Path("reports/missing_game_log_identity_evidence_2027.json")

def main():
    data=json.loads(INPUT.read_text(encoding="utf-8"))
    ids=sorted({r["nba_player_id"] for r in data["players"]})
    session=requests.Session()
    bindings=[]
    for start in range(0,len(ids),40):
        batch=ids[start:start+40]
        for attempt in range(3):
            try:
                bindings.extend(query_wikidata(session,batch))
                break
            except (requests.RequestException,ValueError,KeyError):
                if attempt==2:raise
                time.sleep(2**attempt)
    by_id={pid:[] for pid in ids}
    for b in bindings:
        pid=b["nba"]["value"]
        if pid not in by_id:continue
        raw=b.get("bref",{}).get("value","")
        bref=raw
        if "/" in raw:
            prefix,suffix=raw.split("/",1)
            if len(prefix)==1 and suffix.startswith(prefix):bref=suffix
        by_id[pid].append({"wikidata_item":b["item"]["value"],"bref_id":bref})
    results=[]
    for p in data["players"]:
        matches=by_id[p["nba_player_id"]]
        exact=len(matches)==1 and bool(matches[0]["bref_id"])
        results.append({"nba_player_id":p["nba_player_id"],"game_rows":p["game_rows"],
            "defending_teams":p["defending_teams"],
            "identity_candidates":matches,
            "candidate_status":"single_wikidata_id_pair" if exact else "missing_or_ambiguous",
            "season_position_verified":False,"human_approved":False})
    report={"total_unmatched_players":len(ids),
            "single_identity_candidates":sum(x["candidate_status"]=="single_wikidata_id_pair" for x in results),
            "players":results,"published":False,
            "warning":"Identity candidates are not season-position evidence or human approval."}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("MISSING_GAME_LOG_IDENTITY_EVIDENCE",json.dumps(report))

if __name__=="__main__":main()
