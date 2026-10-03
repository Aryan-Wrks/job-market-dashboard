import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")

# how many jobs got at least one real skill extracted
with_skills = conn.execute("SELECT COUNT(DISTINCT job_id) FROM skills").fetchone()[0]
total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
print(f"Jobs with at least one extracted skill: {with_skills} / {total}")

# the headline finding: top skills across ALL postings
top_skills = pd.read_sql("""
    SELECT skill_name, COUNT(*) AS mentions
    FROM skills
    GROUP BY skill_name
    ORDER BY mentions DESC
    LIMIT 15
""", conn)

print("\n=== Top 15 most in-demand skills ===")
print(top_skills.to_string(index=False))

conn.close()