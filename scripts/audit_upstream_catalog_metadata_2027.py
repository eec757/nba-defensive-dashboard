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
    metadata_columns=[]
    metadata_rows=[]
    if ("main","metadata") in tables:
        metadata_columns=[{"name":name,"type":typ} for name,typ in
            con.execute("SELECT column_name,data_type FROM duckdb_columns() WHERE database_name='nba' AND schema_name='main' AND table_name='metadata' ORDER BY column_index").fetchall()]
        # Bound the sample; metadata can contain opaque internal values.
        sample=con.execute('SELECT * FROM nba.main.metadata LIMIT 10')
        names=[d[0] for d in sample.description]
        metadata_rows=[{k:str(v)[:300] if v is not None else None for k,v in zip(names,row)} for row in sample.fetchall()]
    # Explicitly query relevant datasets instead of relying on the first ten rows.
    relevant_updates=[]
    if ("main","metadata") in tables:
        for dataset,source,updated in con.execute("""
            SELECT dataset, source, CAST(updated AS VARCHAR)
            FROM nba.main.metadata
            WHERE dataset IN ('games','player_box','game_rotations')
            ORDER BY dataset
        """).fetchall():
            relevant_updates.append({"dataset":dataset,"source":source,"updated_utc":updated})
    report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
            "catalog":CATALOG,"metadata_table_candidates":candidates,
            "catalog_table_count":len(tables),
            "metadata_columns":metadata_columns,"metadata_sample_rows":metadata_rows,
            "relevant_dataset_updates":relevant_updates,
            "refresh_cadence_verified":False,
            "note":"Table names are hints only. No upstream refresh cadence inferred from absence or presence of metadata tables.",
            "publication_ready":False}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("UPSTREAM_METADATA",json.dumps(report))

if __name__=="__main__":main()
