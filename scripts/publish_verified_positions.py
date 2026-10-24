"""Publish position-defense only from independently reviewed player ID crosswalk.

Crosswalk CSV columns: bref_id,nba_player_id,position,verification_source,verified
All five positions must have adequate game-log coverage before publication.
"""
import csv
import json
from urllib.parse import urlparse
from collections import defaultdict
from pathlib import Path
import duckdb

CATALOG="https://basketball-data.billmill.org/nba/nba.duckdb"
POSITIONS=("PG","SG","SF","PF","C")
CROSSWALK=Path("data/verified_player_ids_2027.csv")
OUTPUT=Path("data/position_defense_2027.json")
MIN_COVERAGE=.95
TEAM_IDS=dict(zip("ATL BOS BRK CHI CHO CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN NOP NYK OKC ORL PHI PHO POR SAC SAS TOR UTA WAS".split(),
"1610612737 1610612738 1610612751 1610612741 1610612766 1610612739 1610612742 1610612743 1610612765 1610612744 1610612745 1610612754 1610612746 1610612747 1610612763 1610612748 1610612749 1610612750 1610612740 1610612752 1610612760 1610612753 1610612755 1610612756 1610612757 1610612758 1610612759 1610612761 1610612762 1610612764".split()))
if len(TEAM_IDS) != 30 or len(set(TEAM_IDS.values())) != 30:
    raise ValueError("NBA team ID mapping must contain 30 unique teams")

def position_metrics(totals, defending_games):
    """Calculate per-defending-game position totals and shot percentages."""
    if defending_games <= 0:
        raise ValueError("Defending games must be positive")
    if len(totals) != 8:
        raise ValueError("Expected player rows, points, rebounds, assists, FGM, FGA, 3PM, 3PA")
    count, pts, reb, ast, fgm, fga, fg3m, fg3a = totals
    if min(count, pts, reb, ast, fgm, fga, fg3m, fg3a) < 0:
        raise ValueError("Negative counting statistic")
    if fgm > fga or fg3m > fg3a or fg3m > fgm or fg3a > fga:
        raise ValueError("Inconsistent shooting totals")
    return {
        "points_allowed": round(pts / defending_games, 2),
        "rebounds_allowed": round(reb / defending_games, 2),
        "assists_allowed": round(ast / defending_games, 2),
        "fg_pct": round(100 * fgm / fga, 1) if fga else None,
        "three_pct": round(100 * fg3m / fg3a, 1) if fg3a else None,
    }

def main():
    if not CROSSWALK.exists():
        print("No verified crosswalk provided; position defense remains unavailable.")
        return
    with CROSSWALK.open(newline="",encoding="utf-8") as f:
        records=list(csv.DictReader(f))
    required={"bref_id","nba_player_id","position","verification_source","verified"}
    if not records or not required.issubset(records[0]):
        raise ValueError("Crosswalk missing required verified identity fields")
    verified={}
    bref_seen=set()
    for r in records:
        if r["verified"].strip().lower() != "true":
            continue
        pid=r["nba_player_id"].strip()
        bref=r["bref_id"].strip()
        source=r["verification_source"].strip()
        pos=r["position"].strip()
        if not pid.isdigit() or not bref or pos not in POSITIONS or not source.startswith("https://"):
            raise ValueError("Verified entries require numeric NBA ID, BRef ID, valid position and evidence URL")
        # A standalone player profile identifies one player but does not establish
        # the link between a Basketball-Reference ID and an NBA numeric ID.
        domain = (urlparse(source).hostname or "").lower()
        if domain in {"nba.com", "www.nba.com", "basketball-reference.com",
                      "www.basketball-reference.com"}:
            raise ValueError("Single-provider player profile cannot verify cross-source identity")
        if pid in verified or bref in bref_seen:
            raise ValueError("Duplicate verified NBA or BRef identity")
        verified[pid]=pos
        bref_seen.add(bref)
    if not verified:
        print("No independently reviewed entries; nothing published.")
        return
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""
      SELECT p.player_id,p.opp_team_id,p.game_id,p.pts,p.reb,p.ast,p.fgm,p.fga,p.fg3m,p.fg3a
      FROM nba.player_game_logs p JOIN nba.games g
        ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    if not rows:
        raise ValueError("No regular-season logs available")
    covered=sum(str(r[0]) in verified for r in rows)
    coverage=covered/len(rows)
    print(f"Verified game-row coverage: {covered}/{len(rows)} ({coverage:.2%})")
    if coverage < MIN_COVERAGE:
        print("Below 95% independently verified game-row coverage; no publication.")
        return
    # NBA team ID -> abbreviation; keyed by opponent team, not player team.
    team_ids=TEAM_IDS
    names={v:k for k,v in team_ids.items()}
    unknown_opponents={str(row[1]) for row in rows if str(row[1]) not in names}
    if unknown_opponents:
        raise ValueError(f"Unknown opponent team IDs in game logs: {sorted(unknown_opponents)}")
    totals=defaultdict(lambda: [0.0]*8)
    games=defaultdict(set)
    all_team_games=defaultdict(set)
    verified_team_rows=defaultdict(int)
    all_team_rows=defaultdict(int)
    for pid,opp,game_id,pts,reb,ast,fgm,fga,fg3m,fg3a in rows:
        pos=verified.get(str(pid))
        team=names.get(str(opp))
        if not team:
            continue
        all_team_games[team].add(game_id)
        all_team_rows[team]+=1
        if not pos:
            continue
        verified_team_rows[team]+=1
        key=(team,pos)
        games[key].add(game_id)
        values=(pts,reb,ast,fgm,fga,fg3m,fg3a)
        totals[key][0]+=1
        for i,value in enumerate(values,1):
            totals[key][i]+=float(value or 0)
    output={"season":"2026-27","verified_game_row_coverage":round(coverage,4),"teams":{}}
    for team in team_ids:
        output["teams"][team]={}
        for pos in POSITIONS:
            t=totals.get((team,pos))
            n=len(all_team_games.get(team,set()))
            team_coverage=verified_team_rows[team]/all_team_rows[team] if all_team_rows[team] else 0
            if not t or n==0 or team_coverage < MIN_COVERAGE:
                output["teams"][team][pos]=None
                continue
            output["teams"][team][pos]={
                **position_metrics(t,n),
                "coverage":f"{n} defending-team games; {team_coverage:.1%} verified opponent player-game rows",
                "matched_player_games":int(t[0])
            }
    if any(output["teams"][team][pos] is None for team in team_ids for pos in POSITIONS):
        print("Incomplete team/position coverage; no publication.")
        return
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print("Wrote independently verified position-defense output:",OUTPUT)

if __name__=="__main__":
    main()
