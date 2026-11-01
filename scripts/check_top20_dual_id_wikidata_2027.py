"""Check exact NBA and Basketball Reference IDs with Wikidata SPARQL.

Read-only evidence discovery; no player approval or position inference.
"""
import csv
import os
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path("reports")
QUEUE=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
CANDIDATES=ROOT/"proposed_verified_player_ids_2027.csv"
OUT=ROOT/"2027_top20_independent_dual_id_evidence.json"
ENDPOINT="https://query.wikidata.org/sparql"

def query_entities(ids):
    values=" ".join('"'+pid+'"' for pid in ids)
    query=("SELECT ?nba ?item ?bref WHERE { VALUES ?nba { "+values+
           " } ?item <http://www.wikidata.org/prop/direct/P3647> ?nba . "+
           "OPTIONAL { ?item <http://www.wikidata.org/prop/direct/P2685> ?bref . } }")
    url=ENDPOINT+"?"+urllib.parse.urlencode({"query":query,"format":"json"})
    req=urllib.request.Request(url,headers={"User-Agent":"NBA-Defensive-Dashboard/1.0 (public identity evidence audit)","Accept":"application/sparql-results+json"})
    with urllib.request.urlopen(req,timeout=40) as resp:
        return json.load(resp)["results"]["bindings"]

def main():
    priority=json.loads(QUEUE.read_text(encoding="utf-8"))["priority_players"][:20]
    with CANDIDATES.open(newline="",encoding="utf-8") as f: proposed=list(csv.DictReader(f))
    by_id={}
    for row in proposed:by_id.setdefault(str(row.get("nba_player_id","")),set()).add(str(row.get("bref_id","")))
    ids=[str(p["nba_player_id"]) for p in priority]
    grouped={pid:{} for pid in ids}
    error=None
    try:
        if os.environ.get("ENABLE_WIKIDATA_TOP20_QUERY") != "1":
            raise RuntimeError("Wikidata top-20 query paused due to observed HTTP 429; enable explicitly after rate limit recovery")
        for entry in query_entities(ids):
            pid=entry["nba"]["value"]
            if pid not in grouped:continue
            qid=entry["item"]["value"].rsplit("/",1)[-1]
            grouped[pid].setdefault(qid,set())
            if "bref" in entry:grouped[pid][qid].add(entry["bref"]["value"])
    except Exception as exc:error=str(exc)[:300]
    results=[]
    for pid in ids:
        candidate_ids=sorted(by_id.get(pid,set())-{""})
        entities=grouped[pid]
        exact=[{"qid":qid,"bref_ids":sorted(brefs.intersection(candidate_ids)),
                "evidence_url":"https://www.wikidata.org/wiki/"+qid}
               for qid,brefs in entities.items() if brefs.intersection(candidate_ids)]
        status=("source_unavailable" if error else
                "exact_dual_id_evidence_found" if len(entities)==1 and len(exact)==1 else
                "ambiguous_multiple_entities" if len(entities)>1 else
                "nba_id_found_bref_mismatch_or_missing" if entities else
                "no_nba_id_wikidata_statement")
        results.append({"nba_player_id":pid,"candidate_bref_ids":candidate_ids,
            "wikidata_entity_ids":sorted(entities),"exact_dual_id_matches":exact,
            "status":status,"error":error if error else None,
            "exact_2026_27_position_verified":False,"approved":False})
    report={"players_checked":len(results),
        "unique_exact_dual_id_evidence":sum(r["status"]=="exact_dual_id_evidence_found" for r in results),
        "unresolved":sum(r["status"]!="exact_dual_id_evidence_found" for r in results),
        "source_error":error,"position_verified":0,"new_approvals":0,
        "crosswalk_modified":False,"published":False,
        "note":"Exact Wikidata P3647/P2685 co-occurrence is identity evidence only. Season position and owner review are still required.",
        "players":results}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_DUAL_ID_EVIDENCE",json.dumps({k:report[k] for k in
        ("players_checked","unique_exact_dual_id_evidence","unresolved","source_error","new_approvals","published")}))

if __name__=="__main__":main()
