"""Stage exact Wikidata identity evidence without granting publication approval."""
import csv
import json
import os
import time
from collections import defaultdict
from pathlib import Path
import requests

QUEUE = Path("reports/identity_review_queue_2027.csv")
STAGED = Path("reports/wikidata_exact_matches_2027.csv")
EXCEPTIONS = Path("reports/wikidata_identity_exceptions_2027.csv")
SUMMARY = Path("reports/wikidata_evidence_summary_2027.json")
API = "https://query.wikidata.org/sparql"
FIELDS = ["priority","team","roster_name","nba_player_id","bref_id","position",
          "regular_season_games","verification_source","nba_profile_url",
          "bref_profile_url","position_source","reviewed_by","reviewed_on","verified"]
EXCEPTION_FIELDS = ["priority","roster_name","nba_player_id","bref_id","reason","wikidata_items"]

def query_wikidata(session, nba_ids):
    # Restrict query to IDs from the actual roster queue, never search by name.
    ids = " ".join(json.dumps(x) for x in nba_ids)
    sparql = ("SELECT ?item ?nba ?bref WHERE { VALUES ?nba { " + ids +
              " } ?item wdt:P3647 ?nba . OPTIONAL { ?item wdt:P2685 ?bref . } }")
    response = session.get(API, params={"query":sparql,"format":"json"},
                           headers={"User-Agent":"NBAIdentityAudit/1.0 (GitHub Actions; identity review)",
                                    "Accept":"application/sparql-results+json"},
                           timeout=90)
    response.raise_for_status()
    return response.json()["results"]["bindings"]

def classify(rows, bindings):
    by_nba = defaultdict(lambda: defaultdict(set))
    for b in bindings:
        nba = b["nba"]["value"]
        item = b["item"]["value"]
        bref = b.get("bref",{}).get("value")
        # Wikidata P2685 normally stores "h/holmgch01", not "holmgch01".
        if bref and "/" in bref:
            prefix, suffix = bref.split("/",1)
            bref = suffix if len(prefix)==1 and suffix.startswith(prefix) else bref
        if bref:
            by_nba[nba][item].add(bref)
        else:
            by_nba[nba][item]
    exact, exceptions = [], []
    for row in rows:
        nba, bref = row["nba_player_id"].strip(), row["bref_id"].strip()
        items = by_nba.get(nba,{})
        matching = [item for item, values in items.items() if values == {bref}]
        if len(items) == 1 and len(matching) == 1:
            item = matching[0]
            exact.append({
                "priority":row["priority"],"team":row["team"],"roster_name":row["roster_name"],
                "nba_player_id":nba,"bref_id":bref,"position":row["position"],
                "regular_season_games":row["regular_season_games"],
                "verification_source":item,
                "nba_profile_url":row["nba_profile_url"],
                "bref_profile_url":row["bref_profile_url"],
                "position_source":row["season_position_source"],
                "reviewed_by":"eec757","reviewed_on":"2026-10-24",
                "verified":"false"
            })
        else:
            reason = ("missing_wikidata_nba_id" if not items else
                      "ambiguous_wikidata_items" if len(items)>1 else
                      "missing_bref_id" if not next(iter(items.values())) else
                      "bref_id_mismatch_or_ambiguous")
            exceptions.append({"priority":row["priority"],"roster_name":row["roster_name"],
                "nba_player_id":nba,"bref_id":bref,"reason":reason,
                "wikidata_items":";".join(sorted(items))})
    return exact, exceptions

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    with QUEUE.open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError("No candidates available: refusing empty evidence audit")
    nba_ids=sorted({r["nba_player_id"].strip() for r in rows if r["nba_player_id"].strip()})
    session=requests.Session()
    bindings=[]
    try:
        for i in range(0,len(nba_ids),40):
            batch=nba_ids[i:i+40]
            for attempt in range(3):
                try:
                    bindings.extend(query_wikidata(session,batch))
                    break
                except (requests.RequestException,ValueError,KeyError):
                    if attempt==2:
                        raise
                    time.sleep(2**attempt)
        exact,exceptions=classify(rows,bindings)
        status="complete"
    except (requests.RequestException,ValueError,KeyError) as exc:
        # A partial network lookup must never be represented as completed evidence.
        exact=[]
        exceptions=[{"priority":r["priority"],"roster_name":r["roster_name"],
            "nba_player_id":r["nba_player_id"],"bref_id":r["bref_id"],
            "reason":"wikidata_query_incomplete","wikidata_items":""} for r in rows]
        status="lookup_error"
        print("WIKIDATA_LOOKUP_ERROR",str(exc))
    write_csv(STAGED,FIELDS,exact)
    write_csv(EXCEPTIONS,EXCEPTION_FIELDS,exceptions)
    summary={"status":status,"candidates":len(rows),"exact_id_pairs":len(exact),
             "exceptions":len(exceptions),"auto_approved":0,
             "staged_file":str(STAGED),"exceptions_file":str(EXCEPTIONS),
             "warning":"Staged evidence is not approval. Crosswalk unchanged; 95% publication gate remains active."}
    SUMMARY.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print("WIKIDATA_EVIDENCE_MATCH",json.dumps(summary))
    if status!="complete":
        raise RuntimeError("Wikidata lookup incomplete; all candidates retained as exceptions")

if __name__=="__main__":
    main()
