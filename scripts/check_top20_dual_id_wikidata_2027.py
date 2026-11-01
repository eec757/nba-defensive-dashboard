"""Independently cross-check top-20 NBA and Basketball Reference IDs on Wikidata.

Only a single Wikidata entity with exact P3647 and P2685 values qualifies as
an identity evidence match. This never verifies season position or approves a
crosswalk. API/network errors remain exceptions, not matches.
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path("reports")
QUEUE=ROOT/"2027_staged_seven_player_identity_review_priority_queue.json"
CANDIDATES=ROOT/"proposed_verified_player_ids_2027.csv"
OUT=ROOT/"2027_top20_independent_dual_id_evidence.json"
API="https://www.wikidata.org/w/api.php"

def claims(entity,property_id):
    values=[]
    for c in entity.get("claims",{}).get(property_id,[]):
        if c.get("rank")=="deprecated":continue
        v=c.get("mainsnak",{}).get("datavalue",{}).get("value")
        if isinstance(v,str):values.append(v)
    return sorted(set(values))

def request(params):
    url=API+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":"NBADefensiveDashboardEvidenceAudit/1.0 (public research; no automated approvals)","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=12) as resp:
        return json.load(resp)

def main():
    priority=json.loads(QUEUE.read_text(encoding="utf-8"))["priority_players"][:20]
    with CANDIDATES.open(newline="",encoding="utf-8") as f:
        proposed=list(csv.DictReader(f))
    by_id={}
    for r in proposed:by_id.setdefault(str(r.get("nba_player_id","")),set()).add(str(r.get("bref_id","")))
    results=[]
    for p in priority:
        pid=str(p["nba_player_id"])
        row={"nba_player_id":pid,"candidate_bref_ids":sorted(by_id.get(pid,set())-{""}),
            "wikidata_entity_ids":[],"exact_dual_id_matches":[],
            "status":"pending","exact_2026_27_position_verified":False,
            "approved":False}
        try:
            search=request({"action":"query","list":"search",
                "srsearch":'haswbstatement:P3647='+pid,"srnamespace":"0",
                "format":"json","srlimit":"10"})
            # Wikidata entity lookup by external ID: SPARQL search is separate;
            # MediaWiki text search is only candidate discovery, never evidence.
            hits=search.get("query",{}).get("search",[])
            qids=[h["title"] for h in hits if h.get("title","").startswith("Q")]
            if qids:
                entities=request({"action":"wbgetentities","ids":"|".join(qids),
                    "props":"claims","format":"json"}).get("entities",{})
                for qid,entity in entities.items():
                    if pid not in claims(entity,"P3647"):continue
                    row["wikidata_entity_ids"].append(qid)
                    matched=sorted(set(claims(entity,"P2685")) & set(row["candidate_bref_ids"]))
                    if matched:row["exact_dual_id_matches"].append({
                        "qid":qid,"bref_ids":matched,"evidence_url":"https://www.wikidata.org/wiki/"+qid})
            row["status"]="exact_dual_id_evidence_found" if len(row["exact_dual_id_matches"])==1 and len(row["wikidata_entity_ids"])==1 else ("ambiguous_multiple_entities" if len(row["wikidata_entity_ids"])>1 else "no_unique_exact_dual_id_evidence")
        except Exception as exc:
            row["status"]="source_unavailable"
            row["error"]=str(exc)[:240]
        results.append(row)
        time.sleep(0.15)
    report={"players_checked":len(results),
        "unique_exact_dual_id_evidence":sum(r["status"]=="exact_dual_id_evidence_found" for r in results),
        "unresolved":sum(r["status"]!="exact_dual_id_evidence_found" for r in results),
        "position_verified":0,"new_approvals":0,"crosswalk_modified":False,
        "published":False,"note":"Wikidata candidate search can miss records; missing hits are not negative identity proof. Exact source values only; independent 2026-27 position and owner approval still required.",
        "players":results}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_DUAL_ID_EVIDENCE",json.dumps({
        k:report[k] for k in ("players_checked","unique_exact_dual_id_evidence","unresolved","new_approvals","published")}))

if __name__=="__main__":main()
