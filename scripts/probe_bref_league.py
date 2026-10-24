"""One-time, rate-limited validation of Basketball-Reference 2026-27 NBA rosters.

No dashboard statistics are changed. Stop on access restrictions; never bypass them.
"""
import collections
import html.parser
import json
import re
import time
import requests

TEAMS = "ATL BOS BRK CHI CHO CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN NOP NYK OKC ORL PHI PHO POR SAC SAS TOR UTA WAS".split()
POSITIONS = {"PG", "SG", "SF", "PF", "C"}
class Roster(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.table = False
        self.row = None
        self.field = None
        self.rows = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("id") == "roster":
            self.table = True
        elif self.table and tag == "tr":
            self.row = {}
        elif self.table and self.row is not None and tag in ("td", "th"):
            self.field = a.get("data-stat")
            if self.field in ("player", "player_name"):
                self.row["bref_id"] = a.get("data-append-csv", "")
        elif self.table and self.row is not None and tag == "a" and self.field in ("player", "player_name"):
            m = re.search(r"/players/[a-z]/([a-z0-9]+)\.html", a.get("href", ""))
            if m:
                self.row["bref_id"] = m.group(1)
    def handle_data(self, data):
        if self.row is not None and self.field in ("player", "player_name", "pos"):
            self.row[self.field] = self.row.get(self.field, "") + data
    def handle_endtag(self, tag):
        if self.table and tag in ("td", "th"):
            self.field = None
        elif self.table and tag == "tr":
            if self.row and (self.row.get("player") or self.row.get("player_name")) and self.row.get("pos") in POSITIONS:
                self.rows.append(self.row)
            self.row = None
        elif self.table and tag == "table":
            self.table = False

def main():
    results = []
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; NBA-Dashboard-Validation/1.0)"
    for index, team in enumerate(TEAMS):
        if index:
            time.sleep(8)
        url = f"https://www.basketball-reference.com/teams/{team}/2027.html"
        try:
            response = session.get(url, timeout=20)
            print(f"{team}: HTTP {response.status_code}", flush=True)
            if response.status_code in (403, 429):
                print("Access restriction detected; stopping rather than retrying.", flush=True)
                break
            response.raise_for_status()
            parser = Roster()
            parser.feed(response.text)
            counts = collections.Counter(row["pos"] for row in parser.rows)
            ids = sum(bool(row.get("bref_id")) for row in parser.rows)
            record = {"team": team, "players": len(parser.rows), "position_counts": dict(counts), "bref_ids": ids}
            results.append(record)
            print(json.dumps(record), flush=True)
        except requests.RequestException as exc:
            print(f"{team}: request failed ({exc})", flush=True)
            break
    print("SUMMARY", json.dumps({
        "teams_checked": len(results),
        "teams_with_10_players": sum(x["players"] >= 10 for x in results),
        "teams_with_all_five_positions": sum(POSITIONS.issubset(x["position_counts"]) for x in results),
        "total_players": sum(x["players"] for x in results),
        "bref_ids": sum(x["bref_ids"] for x in results),
        "nba_player_id_mapping_verified": False,
        "dashboard_modified": False
    }), flush=True)
    if len(results) != 30 or any(x["players"] < 10 for x in results):
        raise SystemExit("Full-league roster validation incomplete.")

if __name__ == "__main__":
    main()
