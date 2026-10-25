"""Read-only 2026-27 roster evidence for missing game-log identities."""
import json
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from publish_verified_positions import TEAM_IDS,POSITIONS

def main():
    source=Path("reports/missing_game_log_identity_evidence_2027.json")
    report=json.loads(source.read_text(encoding="utf-8"))
    candidates={x["identity_candidates"][0]["bref_id"] for x in report["players"]
                if x["candidate_status"]=="single_wikidata_id_pair"}
    cache=json.loads(Path("reports/season_roster_position_cache_2027.json").read_text(encoding="utf-8"))
    positions={key:[] for key in candidates}
    for url,players in cache.items():
        team=url.split("/teams/")[1].split("/")[0]
        for bref in candidates:
            for pos in players.get(bref,[]):
                if pos in POSITIONS:
                    positions[bref].append({"team":team,"position":pos,"url":url})
    errors={}
    for player in report["players"]:
        matches=player["identity_candidates"]
        bref=matches[0]["bref_id"] if player["candidate_status"]=="single_wikidata_id_pair" else ""
        evidence=positions.get(bref,[])
        player["season_position_evidence"]=evidence
        player["season_position_verified"]=bool(evidence and len({x["position"] for x in evidence})==1 and not errors)
    report["roster_fetch_errors"]=errors
    report["season_positions_supported"]=sum(p["season_position_verified"] for p in report["players"])
    report["published"]=False
    out=Path("reports/missing_player_position_evidence_2027.json")
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("MISSING_PLAYER_POSITION_EVIDENCE",json.dumps({"supported":report["season_positions_supported"],"total":len(report["players"]),"roster_errors":errors,"players":[{"nba_player_id":p["nba_player_id"],"season_position_evidence":p["season_position_evidence"]} for p in report["players"]]}))

if __name__=="__main__":main()
