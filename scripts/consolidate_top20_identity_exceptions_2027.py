"""Consolidate top-20 NBA/BRef/Wikidata evidence and unresolved source exceptions.

Read-only triage. A reachable profile or matching name does not establish an
independent NBA-to-BRef mapping. No automated approvals or crosswalk writes.
"""
import json
from pathlib import Path
ROOT=Path("reports")
OUT=ROOT/"2027_top20_identity_source_exceptions.json"

def read(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def main():
    nba=read("2027_top20_nba_id_identity_checks.json")
    bref=read("2027_top20_direct_profile_review.json")
    wikidata=read("2027_top20_independent_dual_id_evidence.json")
    n={p["nba_player_id"]:p for p in nba["players"]}
    b={p["nba_player_id"]:p for p in bref["players"]}
    w={p["nba_player_id"]:p for p in wikidata["players"]}
    ids=list(n)
    if set(ids)!=set(b) or set(ids)!=set(w):
        raise ValueError("Source reports disagree on priority NBA IDs")
    rows=[]
    for pid in ids:
        br=b[pid]["basketball_reference_candidates"]
        wd=w[pid]
        rows.append({"nba_player_id":pid,
            "nba_api_name":n[pid]["nba_api_player_name"],
            "nba_id_present":n[pid]["nba_id_present_in_nba_api_static"],
            "bref_candidates":[{"bref_id":x["candidate_bref_id"],
                "url":x.get("url"),"status":x["status"],
                "http_status":x.get("http_status"),"title":x.get("title"),
                "heading":x.get("heading")} for x in br],
            "bref_unavailable":any(x["status"]!="reachable" for x in br),
            "wikidata_status":wd["status"],
            "wikidata_source_error":wd.get("error"),
            "exact_dual_id_evidence":wd.get("exact_dual_id_matches",[]),
            "espn_cbs_independent_evidence":"not_yet_checked_at_player_level",
            "review_status":"requires_independent_exact_dual_id_and_season_position",
            "approved":False})
    report={"players":rows,"players_checked":len(rows),
        "players_with_unavailable_bref_candidates":sum(x["bref_unavailable"] for x in rows),
        "players_with_exact_wikidata_evidence":sum(bool(x["exact_dual_id_evidence"]) for x in rows),
        "new_approvals":0,"production_modified":False,"published":False,
        "note":"Source access failures are not identity mismatches; no source title/name check confers approval."}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TOP20_IDENTITY_SOURCE_EXCEPTIONS",json.dumps({k:report[k] for k in
        ("players_checked","players_with_unavailable_bref_candidates",
        "players_with_exact_wikidata_evidence","new_approvals","published")}))
if __name__=="__main__":main()
