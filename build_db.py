import sqlite3

DB_PATH = "jobs.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id               TEXT PRIMARY KEY,
    title                TEXT,
    company              TEXT,
    location             TEXT,
    state                TEXT,
    category             TEXT,
    salary_min           REAL,
    salary_max           REAL,
    salary_is_predicted  INTEGER,
    description          TEXT,
    posted_date          TEXT,
    url                  TEXT,
    search_query         TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    job_id      TEXT,
    skill_name  TEXT,
    PRIMARY KEY (job_id, skill_name),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
"""


def build_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()

    # check what got created
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    print("Tables in database:", [t[0] for t in tables])

    conn.close()


if __name__ == "__main__":
    build_db()