"""Read-only audit of player-game rows not covered by independently supported proposal."""
import csv
import json
from collections import Counter,defaultdict
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG,TEAM_IDS

def main():
    with Path("reports/proposed_verified_player_ids_2027.csv").open(newline="",encoding="utf-8") as f:
        proposal=list(csv.DictReader(f))
    with Path("reports/season_position_evidence_2027.csv").open(newline="",encoding="utf-8") as f:
        evidence=list(csv.DictReader(f))
    supported={(r["nba_player_id"],r["bref_id"]) for r in evidence if r["status"]=="supported"}
    covered={r["nba_player_id"] for r in proposal if r["verified"].strip().lower()=="true"
             and (r["nba_player_id"],r["bref_id"]) in supported}
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""
      SELECT p.player_id,p.opp_team_id,p.game_id
      FROM nba.player_game_logs p JOIN nba.games g
      ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    teams={str(v):k for k,v in TEAM_IDS.items()}
    unmatched=defaultdict(lambda:{"game_rows":0,"defending_teams":Counter(),"game_ids":[]})
    for pid,opp,gid in rows:
        if str(pid) in covered: continue
        team=teams.get(str(opp))
        if not team: raise ValueError(f"Unknown defending team ID {opp}")
        r=unmatched[str(pid)]
        r["game_rows"]+=1
        r["defending_teams"][team]+=1
        r["game_ids"].append(str(gid))
    queue_path=Path("reports/identity_review_queue_2027.csv")
    with queue_path.open(newline="",encoding="utf-8") as f:
        queue=list(csv.DictReader(f))
    by_id=defaultdict(list)
    for candidate in queue:
        by_id[candidate["nba_player_id"]].append(candidate)
    for pid in unmatched:
        matches=by_id.get(pid,[])
        unmatched[pid]["queue_matches"]=[{
            "roster_name":m.get("roster_name",""),
            "bref_id":m.get("bref_id",""),
            "team":m.get("team",""),
            "position":m.get("position",""),
            "position_source":m.get("season_position_source","")
        } for m in matches]
    # Hypothetical coverage only: these records remain unverified.
    all_team_rows=Counter()
    covered_team_rows=Counter()
    for pid,opp,gid in rows:
        team=teams[str(opp)]
        all_team_rows[team]+=1
        if str(pid) in covered:
            covered_team_rows[team]+=1
    baseline_gates=sum(covered_team_rows[t]/all_team_rows[t]>=.95 for t in TEAM_IDS if all_team_rows[t])
    for pid,entry in unmatched.items():
        projected=sum((covered_team_rows[t]+entry["defending_teams"][t])/all_team_rows[t]>=.95
                      for t in TEAM_IDS if all_team_rows[t])
        entry["hypothetical_team_gates_if_verified"]=projected
        entry["potential_new_team_gates"]=projected-baseline_gates
    
    report={"total_game_rows":len(rows),"unmatched_game_rows":sum(r["game_rows"] for r in unmatched.values()),
            "unmatched_player_ids":len(unmatched),"baseline_team_gates":baseline_gates,"hypothetical_only":True,
            "players":[{"nba_player_id":pid,"game_rows":r["game_rows"],"potential_new_team_gates":r["potential_new_team_gates"],"hypothetical_team_gates_if_verified":r["hypothetical_team_gates_if_verified"],
                        "defending_teams":dict(r["defending_teams"]),
                        "game_ids":sorted(set(r["game_ids"])),
                        "review_queue_matches":r["queue_matches"],
                        "in_existing_review_queue":bool(r["queue_matches"])}
                       for pid,r in sorted(unmatched.items(),key=lambda item:(-item[1]["game_rows"],item[0]))],
            "publication_ready":False,
            "note":"Unmatched players are investigation candidates only. No identity or position is inferred."}
    out=Path("reports/unmatched_player_games_2027.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("UNMATCHED_PLAYER_GAMES",json.dumps(report))

if __name__=="__main__":main()
