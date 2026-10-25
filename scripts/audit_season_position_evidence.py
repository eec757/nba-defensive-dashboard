"""Check season-position evidence against actual Basketball-Reference roster cells.

Never infer proof from a URL's shape or a generated roster candidate.
This audit is read-only; failures and missing pages remain exceptions.
"""
import csv
import json
import re
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup, Comment

SOURCE=Path("reports/proposed_verified_player_ids_2027.csv")
OUT=Path("reports/season_position_evidence_2027.csv")
FIELDS=["nba_player_id","bref_id","proposed_position","position_source","observed_position","status","reason"]

def roster_positions(html):
    soup=BeautifulSoup(html,"html.parser")
    # BRef sometimes embeds its tables in HTML comments.
    for comment in soup.find_all(string=lambda x:isinstance(x,Comment)):
        if "<table" in comment:
            nested=BeautifulSoup(str(comment),"html.parser")
            for table in nested.find_all("table"):
                soup.append(table)
    result=defaultdict(set)
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            link=tr.find("a",href=re.compile(r"^/players/[a-z]/[a-z0-9]+\.html$"))
            if not link:
                continue
            cells=tr.find_all(["th","td"])
            pos=next((c.get_text(" ",strip=True) for c in cells
                      if c.get("data-stat") in ("pos","position")),None)
            if pos is None:
                # Roster tables may have a visible 'Pos' header without data-stat.
                headers=[c.get_text(" ",strip=True) for c in table.select("thead tr:last-child th, thead tr:last-child td")]
                if "Pos" in headers:
                    idx=headers.index("Pos")
                    if idx<len(cells):
                        pos=cells[idx].get_text(" ",strip=True)
            if pos:
                result[link["href"].split("/")[-1].removesuffix(".html")].add(pos)
    return result

def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:
        records=list(csv.DictReader(f))
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; NBA research position audit)"})
    cache={}
    results=[]
    # Recheck the previously rate-limited Washington roster first.
    records.sort(key=lambda row: (0 if "/teams/WAS/" in row["position_source"] else 1, row["position_source"], row["bref_id"]))
    for row in records:
        url=row["position_source"]
        if url not in cache:
            try:
                parsed=urlparse(url)
                if parsed.scheme!="https" or parsed.hostname not in ("www.basketball-reference.com","basketball-reference.com") or not re.fullmatch(r"/teams/[A-Z]{3}/2027\.html",parsed.path):
                    raise ValueError("invalid_2027_team_roster_url")
                for attempt in range(3):
                    response=session.get(url,timeout=25)
                    if response.status_code != 429:
                        break
                    time.sleep(5 * (attempt + 1))
                response.raise_for_status()
                cache[url]=roster_positions(response.text)
                time.sleep(2)
            except (requests.RequestException,ValueError) as exc:
                cache[url]=str(exc)
        observed=cache[url]
        if isinstance(observed,str):
            status,reason,positions="unverified","source_unavailable_or_invalid: "+observed,""
        else:
            positions=";".join(sorted(observed.get(row["bref_id"],set())))
            if not positions:
                status,reason="unverified","player_not_found_with_position_on_source"
            elif positions==row["position"]:
                status,reason="supported","exact_2026_27_roster_position"
            else:
                status,reason="exception","position_mismatch_or_multiple_values"
        results.append({"nba_player_id":row["nba_player_id"],"bref_id":row["bref_id"],
                        "proposed_position":row["position"],"position_source":url,
                        "observed_position":positions,"status":status,"reason":reason})
    roster_cache={url:{pid:sorted(values) for pid,values in observed.items()}
                  for url,observed in cache.items() if not isinstance(observed,str)}
    Path("reports/season_roster_position_cache_2027.json").write_text(
        json.dumps(roster_cache,indent=2)+"\\n",encoding="utf-8")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)
    summary={"total":len(results),"supported":sum(r["status"]=="supported" for r in results),
             "exceptions":sum(r["status"]=="exception" for r in results),
             "unverified":sum(r["status"]=="unverified" for r in results),
             "published":False,"report":str(OUT)}
    print("SEASON_POSITION_EVIDENCE",json.dumps(summary))
    if summary["supported"]!=summary["total"]:
        print("POSITION_EVIDENCE_INCOMPLETE: live crosswalk remains unchanged")

if __name__=="__main__":
    main()
