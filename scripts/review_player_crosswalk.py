"""Compare candidate player identities with a documented external crosswalk.

Only explicit source ID pairs are corroboration; name-based crosswalk methods
are not independent proof. Produces review reports, never publishes dashboard data.
"""
import collections
import csv
import io
import json
from pathlib import Path
import requests

SOURCE="https://raw.githubusercontent.com/llimllib/nba_data/main/pipeline/player_ids.csv"
INPUT=Path("reports/player_matching_2027.csv")
OUT=Path("reports")

def main():
    if not INPUT.exists():
        raise FileNotFoundError("Run scripts/audit_league_matching.py first")
    response=requests.get(SOURCE,timeout=30)
    response.raise_for_status()
    external=collections.defaultdict(list)
    for row in csv.DictReader(io.StringIO(response.text)):
        if row.get("source")=="bbref":
            external[row["source_id"]].append(row)
    candidates=list(csv.DictReader(INPUT.open(encoding="utf-8",newline="")))
    results=[]
    for row in candidates:
        links=external.get(row["bref_id"],[])
        equal=[link for link in links if link["player_id"]==row["nba_player_id"]]
        if row["status"]!="single_name_candidate":
            status="no_game_log_candidate"
        elif len(links)!=1:
            status="missing_or_ambiguous_external_crosswalk"
        elif not equal:
            status="external_id_conflict"
        elif links[0]["method"]=="player_page":
            status="source_player_page_link_review_required"
        elif links[0]["method"]=="manual":
            status="source_manual_link_review_required"
        else:
            status="corroborated_but_name_derived"
        results.append({
            **row,"external_nba_id":links[0]["player_id"] if len(links)==1 else "",
            "external_method":links[0]["method"] if len(links)==1 else "",
            "crosswalk_status":status,
            "crosswalk_source":SOURCE
        })
    with (OUT/"player_id_crosswalk_review_2027.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    unresolved=[r for r in results if r["crosswalk_status"]=="missing_or_ambiguous_external_crosswalk"]
    fields=["team","roster_name","position","bref_id","nba_player_id","nba_name","regular_season_games","crosswalk_status","basketball_reference_player_url","nba_player_profile_url","review_status","review_notes"]
    with (OUT/"unresolved_player_ids_2027.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        writer.writeheader()
        for r in unresolved:
            pid=r["nba_player_id"]
            bref=r["bref_id"]
            writer.writerow({**r,
                "basketball_reference_player_url":("https://www.basketball-reference.com/players/"+bref[0]+"/"+bref+".html") if bref else "",
                "nba_player_profile_url":("https://www.nba.com/player/"+pid) if pid else "",
                "review_status":"needs_independent_id_evidence","review_notes":""})
    print("UNRESOLVED ID REVIEW",json.dumps({"count":len(unresolved),"players":[{"team":r["team"],"name":r["roster_name"],"bref_id":r["bref_id"],"nba_id":r["nba_player_id"]} for r in unresolved]}),flush=True)
    # Prioritize review by actual regular-season appearances, not roster size.
    # Every player ID remains unverified until independent evidence is reviewed.
    review=[r for r in results if r["status"]=="single_name_candidate"]
    review.sort(key=lambda r:(r["crosswalk_status"]=="corroborated_but_name_derived",
                              -int(r["regular_season_games"] or 0),r["team"],r["roster_name"]))
    review_fields=["priority","team","roster_name","position","bref_id","nba_player_id",
                   "regular_season_games","crosswalk_status","basketball_reference_player_url",
                   "nba_player_profile_url","independent_evidence_url","identity_reviewed","review_notes"]
    with (OUT/"verification_priority_2027.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=review_fields,extrasaction="ignore")
        writer.writeheader()
        for index,r in enumerate(review,1):
            bref=r["bref_id"]
            pid=r["nba_player_id"]
            writer.writerow({**r,"priority":index,
                "basketball_reference_player_url":("https://www.basketball-reference.com/players/"+bref[0]+"/"+bref+".html") if bref else "",
                "nba_player_profile_url":("https://www.nba.com/player/"+pid) if pid else "",
                "independent_evidence_url":"","identity_reviewed":"false","review_notes":""})
    print("VERIFICATION PRIORITY",json.dumps({
        "total":len(review),
        "unresolved":sum(r["crosswalk_status"]!="corroborated_but_name_derived" for r in review),
        "top_10":[{"team":r["team"],"name":r["roster_name"],
                   "games":int(r["regular_season_games"] or 0),
                   "status":r["crosswalk_status"]} for r in review[:10]],
        "publication_ready":False
    }),flush=True)
    counts=collections.Counter(row["crosswalk_status"] for row in results)
    summary={"roster_entries":len(results),"status_counts":dict(counts),
      "note":"Crosswalk source includes name-derived mappings. Matching numeric IDs is corroboration, not necessarily independent verification. No positions published.",
      "source":SOURCE}
    (OUT/"player_id_crosswalk_review_summary_2027.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print("CROSSWALK REVIEW SUMMARY",json.dumps(summary),flush=True)

if __name__=="__main__":
    main()
