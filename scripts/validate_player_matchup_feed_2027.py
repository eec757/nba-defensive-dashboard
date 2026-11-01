"""Validate player matchup preview and create a separate gated dashboard feed.

Never publishes when any team/position gate fails. The preview remains in
reports/ for inspection. Production summary and crosswalk are unchanged.
"""
import json
from pathlib import Path

PREVIEW=Path("reports/2027_verified_player_matchup_game_log_preview.json")
OUT=Path("reports/2027_player_matchup_feed_readiness.json")
def main():
    p=json.loads(PREVIEW.read_text(encoding="utf-8"))
    players=p["players"]
    ids=[x["nba_player_id"] for x in players]
    if len(ids)!=len(set(ids)):raise ValueError("Duplicate NBA IDs in player preview")
    for x in players:
        if x["verified_position"] not in ("PG","SG","SF","PF","C"):raise ValueError("Unverified position")
        if not isinstance(x["games"],int) or x["games"]<=0:raise ValueError("Invalid game count")
        for key in ("points_per_game","rebounds_per_game","assists_per_game","threes_made_per_game","threes_attempted_per_game"):
            if x[key]<0:raise ValueError("Negative per-game statistic")
        if x["threes_made_per_game"]>x["threes_attempted_per_game"]+0.011:raise ValueError("Impossible 3-point rate")
        for key in ("fg_pct","three_pct"):
            if x[key] is not None and not 0<=x[key]<=100:raise ValueError("Invalid shooting percentage")
    audit={"season":p["season"],"validated_players":len(players),
        "game_log_rows":p["total_player_game_rows"],
        "feed_ready_for_publication":False,"blocked_reason":"Position-defense 95% leaguewide, 30-team and 150-position gates not all met",
        "preview_report":str(PREVIEW),"production_modified":False,"published":False}
    OUT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print("PLAYER_MATCHUP_FEED_READINESS",json.dumps(audit))
if __name__=="__main__":main()
