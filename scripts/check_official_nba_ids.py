"""Independently check candidate NBA numeric IDs against nba_api's NBA player directory.
This validates NBA-side ID/name only, NOT the Basketball-Reference-to-NBA identity link.
Never changes verified flags or publishes dashboard statistics.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path
from nba_api.stats.static import players

SOURCE = Path("reports/verification_priority_2027.csv")
OUT = Path("reports/nba_official_id_name_check_2027.csv")
MISMATCHES = Path("reports/nba_id_mismatch_review_2027.csv")
SUMMARY = Path("reports/nba_official_id_name_summary_2027.json")

def normalize(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"\\(TW\\)", "", value, flags=re.I)
    value = re.sub(r"\\b(jr|sr|ii|iii|iv)\\b", "", value, flags=re.I)
    return re.sub(r"[^a-z0-9]", "", value.lower())

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing {SOURCE}; run crosswalk review first")
    with SOURCE.open(newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    if not records:
        raise ValueError("Empty verification-priority report")
    nba_by_id = {str(p["id"]): p for p in players.get_players()}
    result = []
    counts = {}
    for r in records:
        pid = (r.get("nba_player_id") or r.get("nba_id") or "").strip()
        name = (r.get("roster_name") or r.get("name") or r.get("player_name") or "").strip()
        entry = nba_by_id.get(pid)
        official_name = entry["full_name"] if entry else ""
        status = ("id_not_in_nba_directory" if not entry else
                  "nba_id_name_match" if normalize(name) == normalize(official_name)
                  else "nba_id_name_mismatch")
        counts[status] = counts.get(status, 0) + 1
        result.append({
            "team": r.get("team", ""), "candidate_name": name,
            "candidate_nba_id": pid, "nba_directory_name": official_name,
            "nba_id_name_status": status,
            "nba_profile_url": f"https://www.nba.com/player/{pid}" if pid.isdigit() else "",
            "bref_id": r.get("bref_id", ""),
            "bref_nba_link_independently_verified": "false",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(result[0]))
        writer.writeheader()
        writer.writerows(result)
    mismatches = [row for row in result if row["nba_id_name_status"] != "nba_id_name_match"]
    for row in mismatches:
        row["possible_name_variant"] = str(normalize(row["candidate_name"]) in normalize(row["nba_directory_name"]) or normalize(row["nba_directory_name"]) in normalize(row["candidate_name"])).lower()
        row["review_decision"] = "needs_human_review"
        row["independent_evidence_url"] = ""
    if mismatches:
        with MISMATCHES.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(mismatches[0]))
            writer.writeheader()
            writer.writerows(mismatches)
    print("NBA NAME MISMATCH REVIEW", json.dumps(mismatches), flush=True)
    summary = {"candidates": len(result), "status_counts": counts,
               "independent_bref_to_nba_link_verified": 0,
               "publication_ready": False,
               "note": "NBA ID/name validation does not independently link BRef IDs to NBA IDs."}
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("OFFICIAL NBA ID CHECK", json.dumps(summary))

if __name__ == "__main__":
    main()
