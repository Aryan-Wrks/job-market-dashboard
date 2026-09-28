import sqlite3
import json
import glob
import os

DB_PATH = "jobs.db"
RAW_DIR = "data/raw"


def get_search_query(path):
    """'data_analyst_20260927_155210.json' -> 'data analyst'"""
    name = os.path.splitext(os.path.basename(path))[0]
    query = name.rsplit("_", 2)[0]        # drop the date and time parts
    return query.replace("_", " ")


def clean_job(job, search_query):
    """Turn one nested Adzuna job into a flat tuple ready for SQL."""
    area = job.get("location", {}).get("area", [])
    state = area[1] if len(area) > 1 else None

    return (
        job["id"],
        job.get("title"),
        job.get("company", {}).get("display_name"),
        job.get("location", {}).get("display_name"),
        state,
        job.get("category", {}).get("label"),
        job.get("salary_min"),
        job.get("salary_max"),
        int(job.get("salary_is_predicted", 0)),
        job.get("description"),
        (job.get("created") or "")[:10],      # '2026-09-07T18:37:51Z' -> '2026-09-07'
        job.get("redirect_url"),
        search_query,
    )


def load_data():
    conn = sqlite3.connect(DB_PATH)
    before = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    files = glob.glob(f"{RAW_DIR}/*.json")
    seen = 0

    for path in files:
        search_query = get_search_query(path)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for job in data["results"]:
            conn.execute(
                "INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                clean_job(job, search_query),
            )
            seen += 1

    conn.commit()
    after = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    conn.close()

    print(f"Files read: {len(files)}")
    print(f"Jobs seen in files: {seen}")
    print(f"New rows added: {after - before}")
    print(f"Total rows in database: {after}")


if __name__ == "__main__":
    load_data()
    