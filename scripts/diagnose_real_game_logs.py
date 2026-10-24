"""Read-only diagnostic of live NBA game-log aggregation.

This script never marks identities verified and never publishes dashboard data.
"""
import json
import csv
from collections import Counter
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG, TEAM_IDS, summarize_position_rows

def main():
    db = duckdb.connect()
    db.execute("INSTALL httpfs; LOAD httpfs;")
    db.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    rows = db.execute("""
        SELECT p.player_id,p.opp_team_id,p.game_id,p.pts,p.reb,p.ast,
               p.fgm,p.fga,p.fg3m,p.fg3a
        FROM nba.player_game_logs p
        JOIN nba.games g ON p.season=g.season AND p.game_id=g.game_id
        WHERE p.season=2027 AND g.game_type='regular_season'
    """).fetchall()
    if not rows:
        raise ValueError("No 2026-27 regular-season game logs available")
    totals, games, covered, all_rows = summarize_position_rows(rows, {}, TEAM_IDS)
    if totals or covered:
        raise AssertionError("Unverified identities unexpectedly aggregated")
    active = {team: len(ids) for team, ids in games.items() if ids}
    if len(active) != 30:
        raise ValueError(f"Expected game logs for 30 teams; found {len(active)}")
    if any(all_rows[team] <= 0 for team in TEAM_IDS):
        raise ValueError("Missing opponent player-game rows for one or more teams")
    frequency = Counter(str(row[0]) for row in rows)
    candidate_file = Path("reports/player_matching_2027.csv")
    candidates = {}
    if candidate_file.exists():
        with candidate_file.open(encoding="utf-8", newline="") as handle:
            for candidate in csv.DictReader(handle):
                pid = candidate.get("nba_player_id", "")
                if pid and candidate.get("status") == "single_name_candidate":
                    candidates[pid] = candidate
    candidate_report_available = candidate_file.exists()
    if candidate_report_available and not candidates:
        raise ValueError("Roster audit produced no single-name player candidates")
    top = []
    for player_id, game_rows in frequency.most_common(25):
        candidate = candidates.get(player_id, {})
        top.append({
            "nba_player_id": player_id,
            "player_game_rows": game_rows,
            "candidate_bref_id": candidate.get("bref_id", ""),
            "candidate_name": candidate.get("roster_name", ""),
            "candidate_position": candidate.get("position", ""),
            "identity_verified": False,
            "candidate_status": "unverified_candidate" if candidate else "candidate_report_unavailable",
        })
    priority_path = Path("reports/game_log_identity_priority_2027.csv")
    priority_path.parent.mkdir(parents=True, exist_ok=True)
    with priority_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "nba_player_id", "player_game_rows", "candidate_name",
            "candidate_bref_id", "candidate_position", "candidate_status",
            "identity_verified"
        ])
        writer.writeheader()
        writer.writerows(top)
    print(f"IDENTITY_PRIORITY_REPORT {priority_path} ({len(top)} candidates)")
    crosswalk_path = Path("data/verified_player_ids_2027.csv")
    crosswalk = list(csv.DictReader(crosswalk_path.open(encoding="utf-8", newline=""))) if crosswalk_path.exists() else []
    staged_ids = {r["nba_player_id"].strip() for r in crosswalk if r.get("nba_player_id")}
    approved_ids = {r["nba_player_id"].strip() for r in crosswalk if r.get("verified", "").strip().lower() == "true"}
    staged_rows = sum(frequency.get(pid, 0) for pid in staged_ids)
    approved_rows = sum(frequency.get(pid, 0) for pid in approved_ids)
    print("IDENTITY_COVERAGE", json.dumps({
        "game_log_rows": len(rows),
        "staged_player_ids": len(staged_ids),
        "staged_game_rows": staged_rows,
        "staged_game_row_coverage_pct": round(100 * staged_rows / len(rows), 2),
        "approved_player_ids": len(approved_ids),
        "approved_game_rows": approved_rows,
        "approved_game_row_coverage_pct": round(100 * approved_rows / len(rows), 2),
        "publication_threshold_pct": 95,
        "staged_is_not_verified": True
    }, sort_keys=True))
    report = {
        "season": "2026-27",
        "player_game_rows": len(rows),
        "active_defending_teams": len(active),
        "defending_team_games": dict(sorted(active.items())),
        "unique_player_ids": len(frequency),
        "top_25_verification_candidates": top,
        "candidate_report_available": candidate_report_available,
        "matched_top_25_candidates": sum(bool(entry["candidate_bref_id"]) for entry in top),
        "candidate_rows_loaded": len(candidates),
        "total_defending_team_games": sum(active.values()),
        "opponent_player_rows_by_team": dict(sorted(all_rows.items())),
        "unknown_opponent_ids": [],
        "position_statistics_published": False,
        "note": "Read-only data diagnostics; no player positions inferred or verified."
    }
    print("REAL_GAME_LOG_DIAGNOSTIC", json.dumps(report, sort_keys=True))
    if not candidate_report_available:
        print("CROSSWALK_NOTE: reports/player_matching_2027.csv is generated by the separate roster audit and is not checked into the repository. NBA player IDs and appearances are valid; candidate names, positions and BRef IDs are unavailable in this run.")

if __name__ == "__main__":
    main()
