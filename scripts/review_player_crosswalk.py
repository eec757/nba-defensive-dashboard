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
    counts=collections.Counter(row["crosswalk_status"] for row in results)
    summary={"roster_entries":len(results),"status_counts":dict(counts),
      "note":"Crosswalk source includes name-derived mappings. Matching numeric IDs is corroboration, not necessarily independent verification. No positions published.",
      "source":SOURCE}
    (OUT/"player_id_crosswalk_review_summary_2027.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print("CROSSWALK REVIEW SUMMARY",json.dumps(summary),flush=True)

if __name__=="__main__":
    main()
