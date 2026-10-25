"""Read-only upstream DuckDB metadata snapshot for diagnosing refresh lag.

This script does not ingest games, modify crosswalks, or publish data.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import duckdb
from publish_verified_positions import CATALOG

OUT=Path("reports/2027_upstream_catalog_metadata.json")

def main():
    con=duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(f"ATTACH '{CATALOG}' AS nba (READ_ONLY)")
    # Query only source catalog metadata, not inferred update schedules.
    tables=con.execute("""SELECT schema_name,table_name FROM duckdb_tables()
        WHERE database_name = 'nba' ORDER BY schema_name,table_name""").fetchall()
    candidates=[{"schema":s,"table":t} for s,t in tables if any(k in t.lower() for k in ("metadata","refresh","update","ingest","source","sync"))]
    report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
            "catalog":CATALOG,"metadata_table_candidates":candidates,
            "catalog_table_count":len(tables),
            "refresh_cadence_verified":False,
            "note":"Table names are hints only. No upstream refresh cadence inferred from absence or presence of metadata tables.",
            "publication_ready":False}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("UPSTREAM_METADATA",json.dumps(report))

if __name__=="__main__":main()
