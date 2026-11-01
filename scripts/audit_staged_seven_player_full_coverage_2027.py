"""Stage a complete seven-player-promoted crosswalk and audit actual game-log coverage.

Never overwrite the production crosswalk or position-defense JSON. Reuses the
independently validated seven-player preview; no approval is synthesized.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
from publish_verified_positions import (CROSSWALK, CATALOG, TEAM_IDS, POSITIONS,
    MIN_COVERAGE, conservative_position_coverage, validate_crosswalk_source,
    validate_independent_evidence)

PREVIEW=Path("reports/2027_seven_player_approved_promotion_preview.csv")
STAGED=Path("reports/2027_staged_verified_player_ids_with_seven.csv")
REPORT=Path("reports/2027_staged_seven_player_full_coverage_audit.json")
EXPECTED={"1626171","1641713","1641842","1643515","1629057","1642383","1641747"}

def load(path):
    with path.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        return reader.fieldnames,list(reader)

def build_staged():
    fields,existing=load(CROSSWALK)
    preview_fields,added=load(PREVIEW)
    if fields!=preview_fields:raise ValueError("Preview columns differ from verified crosswalk")
    if len(added)!=7 or {r["nba_player_id"] for r in added}!=EXPECTED:
        raise ValueError("Approved seven-player preview incomplete")
    combined=existing+added
    nba_ids=[r["nba_player_id"] for r in combined]
    bref_ids=[r["bref_id"] for r in combined]
    if len(set(nba_ids))!=len(nba_ids) or len(set(bref_ids))!=len(bref_ids):
        raise ValueError("Staged crosswalk has duplicate IDs")
    verified={}
    for r in combined:
        if r["verified"].strip().lower()!="true":continue
        validate_crosswalk_source(r["verification_source"])
        validate_independent_evidence(r)
        if r["position"] not in POSITIONS:raise ValueError("Invalid exact position")
        verified[r["nba_player_id"]]=r["position"]
    if any(pid not in verified for pid in EXPECTED):
        raise ValueError("One or more approved players missing from verified staging")
    STAGED.parent.mkdir(parents=True,exist_ok=True)
    with STAGED.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(combined)
    return verified

def audit(rows,verified):
    lookup={str(v):k for k,v in TEAM_IDS.items()}
    total=len(rows)
    if not total:raise ValueError("No current regular-season game rows")
    by_team=defaultdict(lambda:{"all":0,"known":0,"positions":defaultdict(int),"games":set()})
    known=0
    for pid,opp,game in rows:
        if str(opp) not in lookup:raise ValueError(f"Unknown defending team ID: {opp}")
        s=by_team[lookup[str(opp)]];s["all"]+=1;s["games"].add(str(game))
        pos=verified.get(str(pid))
        if pos:s["known"]+=1;s["positions"][pos]+=1;known+=1
    league_pass=known/total>=MIN_COVERAGE
    teams={};failed=[]
    for team in TEAM_IDS:
        s=by_team[team]
        team_rate=s["known"]/s["all"] if s["all"] else 0
        team_pass=bool(s["games"] and team_rate>=MIN_COVERAGE)
        unknown=s["all"]-s["known"]
        positions={}
        for pos in POSITIONS:
            exact=s["positions"][pos]
            rate=conservative_position_coverage(exact,unknown)
            passed=bool(exact and team_pass and league_pass and rate>=MIN_COVERAGE)
            positions[pos]={"verified_rows":exact,"unknown_rows_in_denominator":unknown,
                            "conservative_coverage_pct":round(100*rate,3),"pass":passed}
            if not passed:failed.append({"team":team,"position":pos})
        teams[team]={"all_rows":s["all"],"verified_rows":s["known"],"unknown_rows":unknown,
                     "coverage_pct":round(100*team_rate,3),"team_gate_pass":team_pass,
                     "defending_games":len(s["games"]),"positions":positions}
    return {"scope":"actual source game rows with staged seven-player crosswalk",
            "all_game_rows":total,"verified_game_rows":known,
            "leaguewide_coverage_pct":round(100*known/total,3),"leaguewide_gate_pass":league_pass,
            "team_gates_passing":sum(t["team_gate_pass"] for t in teams.values()),
            "position_cells_passing":150-len(failed),"failed_position_cells":failed,
            "teams":teams,"publication_ready":league_pass and not failed,
            "published":False,"production_crosswalk_modified":False,
            "production_position_defense_modified":False}

def main():
    verified=build_staged()
    import duckdb
    db=duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows=db.execute("""SELECT p.player_id,p.opp_team_id,p.game_id
      FROM nba.player_game_logs p JOIN nba.games g
        ON p.season=g.season AND p.game_id=g.game_id
      WHERE p.season=2027 AND g.game_type='regular_season'""").fetchall()
    report=audit(rows,verified)
    REPORT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("STAGED_SEVEN_FULL_COVERAGE_AUDIT",json.dumps({
        k:report[k] for k in ("all_game_rows","verified_game_rows","leaguewide_coverage_pct",
        "leaguewide_gate_pass","team_gates_passing","position_cells_passing","publication_ready","published")}))
    if not report["publication_ready"]:
        print("STAGED_CROSSWALK_PUBLICATION_BLOCKED: 95 percent gates not all met")

if __name__=="__main__":main()
