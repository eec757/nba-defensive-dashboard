"""One-page, low-volume Basketball-Reference access and roster schema probe.

Diagnostic only. Never publish scraped data into the dashboard.
"""
import re
import requests
from html.parser import HTMLParser

URL = "https://www.basketball-reference.com/teams/OKC/2027.html"

class RosterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_roster = False
        self.in_row = False
        self.field = None
        self.row = {}
        self.rows = []
        self.player_ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("id") == "roster":
            self.in_roster = True
        elif self.in_roster and tag == "tr":
            self.in_row = True
            self.row = {}
        elif self.in_roster and self.in_row and tag in ("th", "td"):
            self.field = a.get("data-stat")
        elif self.in_roster and self.in_row and tag == "a" and self.field in ("player", "player_name"):
            href = a.get("href", "")
            if re.match(r"^/players/[a-z]/[a-z0-9]+\\.html$", href):
                self.row["bref_id"] = href.split("/")[-1].removesuffix(".html")
    def handle_data(self, data):
        if self.in_roster and self.in_row and self.field in ("player", "player_name", "pos"):
            self.row[self.field] = self.row.get(self.field, "") + data
    def handle_endtag(self, tag):
        if self.in_roster and tag in ("th", "td"):
            self.field = None
        elif self.in_roster and tag == "tr":
            if self.row.get("player") or self.row.get("player_name"):
                self.rows.append(self.row)
            self.in_row = False
        elif self.in_roster and tag == "table":
            self.in_roster = False

def main():
    try:
        r = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0 (compatible; NBA-Dashboard-Validation/1.0)"})
        print(f"Basketball-Reference OKC 2027: HTTP {r.status_code}, bytes={len(r.content)}", flush=True)
        r.raise_for_status()
        p = RosterParser()
        p.feed(r.text)
        print(f"Roster entries: {len(p.rows)}", flush=True)
        print("Position counts:", {pos: sum(x.get("pos", "").strip() == pos for x in p.rows) for pos in ("PG","SG","SF","PF","C")}, flush=True)
        print(f"Basketball-Reference player IDs: {sum(bool(x.get('bref_id')) for x in p.rows)}", flush=True)
        print("Sample player/position:", [(x.get("player") or x.get("player_name"), x.get("pos")) for x in p.rows[:3]], flush=True)
        if len(p.rows) < 10 or sum(bool(x.get("pos")) for x in p.rows) < 10:
            raise ValueError("Roster table missing or insufficient position coverage")
        print("Single-team roster access and position schema verified; NBA-ID matching and 30-team coverage NOT verified.", flush=True)
    except Exception as e:
        print(f"Basketball-Reference validation failed: {type(e).__name__}: {e}", flush=True)
        raise

if __name__ == "__main__":
    main()
