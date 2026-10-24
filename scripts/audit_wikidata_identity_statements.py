"""Read-only Wikidata identity statement audit; never approves or publishes players."""
import csv
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

SOURCE = Path("data/verified_player_ids_2027.csv")
OUTPUT = Path("reports/wikidata_identity_statements_2027.csv")
ENTITY = re.compile(r"^/wiki/(Q[1-9][0-9]*)/?$")
FIELDS = ["nba_player_id", "bref_id", "wikidata_entity", "nba_statement_match",
          "bref_statement_match", "result", "detail"]


def statement_values(entity, property_id):
    claims = entity.get("claims", {}).get(property_id, [])
    values = set()
    for claim in claims:
        if claim.get("rank") == "deprecated":
            continue
        value = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(value, str):
            values.add(value)
    return values


def check(row, session):
    url = (row.get("verification_source") or "").strip()
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in {"www.wikidata.org", "wikidata.org"}:
        return None
    match = ENTITY.fullmatch(parsed.path)
    if not match:
        return dict(result="invalid_wikidata_url", detail="Expected /wiki/Q-number", wikidata_entity="")
    qid = match.group(1)
    result = dict(wikidata_entity=qid)
    try:
        response = session.get(
            f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json",
            headers={"User-Agent": "NBA-Defensive-Dashboard-Identity-Audit/1.0 (GitHub project)"},
            timeout=20,
        )
        response.raise_for_status()
        entities = response.json()["entities"]
        entity = entities.get(qid)
        if not entity or entity.get("missing") is not None:
            return dict(result, result="entity_missing", detail="Entity not found")
        nba = statement_values(entity, "P3647")
        bref = statement_values(entity, "P2685")
        nba_match = row["nba_player_id"].strip() in nba
        bref_match = row["bref_id"].strip() in bref
        result.update(nba_statement_match=str(nba_match).lower(),
                      bref_statement_match=str(bref_match).lower(),
                      result="both_ids_match" if nba_match and bref_match else "id_mismatch",
                      detail=f"NBA IDs: {sorted(nba)}; BRef IDs: {sorted(bref)}")
    except (requests.RequestException, ValueError, KeyError) as exc:
        result.update(result="lookup_error", detail=str(exc)[:250])
    return result


def main():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    session = requests.Session()
    report = []
    for row in rows:
        check_result = check(row, session)
        if check_result is not None:
            report.append({"nba_player_id": row["nba_player_id"],
                           "bref_id": row["bref_id"],
                           "nba_statement_match": "",
                           "bref_statement_match": "",
                           **check_result})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report)
    print("WIKIDATA_IDENTITY_AUDIT", json.dumps({
        "records_checked": len(report),
        "both_ids_match": sum(r["result"] == "both_ids_match" for r in report),
        "mismatch": sum(r["result"] == "id_mismatch" for r in report),
        "lookup_errors": sum(r["result"] == "lookup_error" for r in report),
        "report": str(OUTPUT),
        "note": "Statement matches are candidates for human review, not approvals."
    }))


if __name__ == "__main__":
    main()
