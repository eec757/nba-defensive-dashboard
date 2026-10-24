"""Manual league-wide roster-to-game-log matching audit; never publishes inferred stats."""
import collections
import csv
import html
import json
import re
import time
import unicodedata
from pathlib import Path

import duckdb
import requests
from probe_bref_league import Roster, TEAMS

CATALOG = "https://basketball-data.billmill.org/nba/nba.duckdb"
TEAM_IDS = dict(zip(TEAMS, [
    "1610612737","1610612738","1610612751","1610612741","1610612766",
    "1610612739","1610612742","1610612743","1610612765","1610612744",
    "1610612745","1610612754","1610612746","1610612747","1610612763",
    "1610612748","1610612749","1610612750","1610612740","1610612752",
    "1610612760","1610612753","1610612755","1610612756","1610612757",
    "1610612758","1610612759","1610612761","1610612762","1610612764"
]))

def normalize(value):
    value = html.unescape(str(value or "")).replace("\u00a0", " ")
    value = re.sub(r"\(TW\)", "", value, flags=re.I)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", value.casefold())

def main():
    out = Path("reports")
    out.mkdir(exist_ok=True)
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    logs = db.execute("""
        SELECT p.player_id, x.name, p.team_id, count(*) AS games
        FROM nba.player_game_logs p
        JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
        JOIN nba.players x ON p.player_id=x.player_id
        WHERE p.season=2027 AND g.game_type='regular_season'
        GROUP BY 1,2,3
    """).fetchall()
    by_team_name = collections.defaultdict(list)
    for pid, name, tid, games in logs:
        by_team_name[(str(tid), normalize(name))].append((str(pid), name, games))
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; NBA-Dashboard-Validation/1.0)"
    records = []
    for index, team in enumerate(TEAMS):
        if index:
            time.sleep(8)
        response = session.get(f"https://www.basketball-reference.com/teams/{team}/2027.html", timeout=25)
        print(team, response.status_code, flush=True)
        if response.status_code in (403,429):
            raise RuntimeError("Website access restricted; audit stopped without retry")
        response.raise_for_status()
        response.encoding = "utf-8"
        parser = Roster()
        parser.feed(response.text)
        if len(parser.rows) < 10:
            raise RuntimeError(f"{team}: roster incomplete ({len(parser.rows)} players)")
        for player in parser.rows:
            name = (player.get("player") or player.get("player_name") or "").strip()
            matches = by_team_name[(TEAM_IDS[team], normalize(name))]
            status = "single_name_candidate" if len(matches)==1 else ("ambiguous" if len(matches)>1 else "no_team_game_log_match")
            records.append({
                "team":team, "roster_name":name, "position":player["pos"],
                "bref_id":player.get("bref_id",""),
                "status":status,
                "nba_player_id":matches[0][0] if len(matches)==1 else "",
                "nba_name":matches[0][1] if len(matches)==1 else "",
                "regular_season_games":matches[0][2] if len(matches)==1 else 0,
                "candidate_ids":";".join(m[0] for m in matches),
            })
        print(team, "roster:",len(parser.rows),"single-name candidates:",sum(r["status"]=="single_name_candidate" for r in records if r["team"]==team),flush=True)
    with (out/"player_matching_2027.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    counts=collections.Counter(r["status"] for r in records)
    matched={(r["team"],r["nba_player_id"]) for r in records if r["status"]=="single_name_candidate"}
    game_rows_matched=sum(games for pid,name,tid,games in logs if any((team,pid) in matched for team,team_id in TEAM_IDS.items() if team_id==str(tid)))
    # Defensive production by opponent position: audit preview only.
    # A name/team match is NOT a verified cross-source identity link.
    candidate_map = {}
    collisions = set()
    for row in records:
        if row["status"] != "single_name_candidate":
            continue
        key = (TEAM_IDS[row["team"]], row["nba_player_id"])
        if key in candidate_map and candidate_map[key] != row["position"]:
            collisions.add(key)
        candidate_map[key] = row["position"]
    for key in collisions:
        candidate_map.pop(key, None)
    detail = db.execute("""
        SELECT p.player_id, p.team_id, p.opp_team_id, p.game_id,
               p.pts, p.reb, p.ast, p.fg3m, p.fg3a, p.fgm, p.fga
        FROM nba.player_game_logs p
        JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    opponents = {value: key for key, value in TEAM_IDS.items()}
    aggregates = collections.defaultdict(lambda: [0.0]*8)
    for pid, tid, opp, game_id, pts, reb, ast, threes, attempts3, fgm, fga in detail:
        position = candidate_map.get((str(tid), str(pid)))
        defense_team = opponents.get(str(opp))
        if not position or not defense_team:
            continue
        key = (defense_team, position)
        bucket = aggregates[key]
        bucket[0] += 1  # matched player-game rows, NOT team games
        for i, value in enumerate((pts, reb, ast, threes, attempts3, fgm, fga), start=1):
            bucket[i] += float(value or 0)
    preview = []
    for (team, pos), totals in sorted(aggregates.items()):
        count = int(totals[0])
        preview.append({
            "defending_team": team, "opponent_position": pos,
            "matched_player_game_rows": count,
            "opponent_pts_total": round(totals[1], 2),
            "opponent_reb_total": round(totals[2], 2),
            "opponent_ast_total": round(totals[3], 2),
            "opponent_3pm_total": round(totals[4], 2),
            "opponent_3pa_total": round(totals[5], 2),
            "opponent_fgm_total": round(totals[6], 2),
            "opponent_fga_total": round(totals[7], 2),
            "identity_status": "unverified_name_team_candidate",
        })
    if preview:
        with (out/"defense_by_position_PREVIEW_UNVERIFIED_2027.csv").open("w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(preview[0]))
            writer.writeheader()
            writer.writerows(preview)
    print("DEFENSE PREVIEW", json.dumps({
        "team_position_groups": len(preview),
        "matched_player_game_rows": sum(row["matched_player_game_rows"] for row in preview),
        "identity_verified": False,
        "published_to_dashboard": False
    }), flush=True)
    summary={
        "season":"2026-27","teams_checked":len(TEAMS),"roster_entries":len(records),
        "match_status_counts":dict(counts),
        "regular_season_game_rows":sum(x[3] for x in logs),
        "game_rows_with_single_name_candidate":game_rows_matched,
        "game_row_coverage_pct":round(100*game_rows_matched/sum(x[3] for x in logs),2) if logs else 0,
        "identity_verified_by_shared_id":0,
        "position_defense_preview_groups":len(preview),
        "position_defense_preview_status":"UNVERIFIED - NOT FOR DASHBOARD",
        "warning":"Name + team matches are candidates, NOT independently verified identity mappings. No dashboard data changed."
    }
    (out/"player_matching_summary_2027.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print("MATCHING AUDIT SUMMARY",json.dumps(summary),flush=True)
    print("Unmatched or ambiguous examples:",[(r["team"],r["roster_name"],r["status"]) for r in records if r["status"]!="single_name_candidate"][:25],flush=True)

if __name__=="__main__":
    main()
