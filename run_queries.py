import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")

def run(title, sql):
    print(f"\n=== {title} ===")
    print(pd.read_sql(sql, conn).to_string(index=False))


run("Jobs per search query", """
    SELECT search_query, COUNT(*) AS jobs
    FROM jobs
    GROUP BY search_query
    ORDER BY jobs DESC
""")

run("Top 10 states by job count", """
    SELECT state, COUNT(*) AS jobs
    FROM jobs
    GROUP BY state
    ORDER BY jobs DESC
    LIMIT 10
""")

run("Top 10 companies hiring", """
    SELECT company, COUNT(*) AS jobs
    FROM jobs
    WHERE company IS NOT NULL AND company != ''
    GROUP BY company
    ORDER BY jobs DESC
    LIMIT 10
""")

run("Average salary by search query", """
    SELECT search_query, AVG(salary_min) AS avg_salary, COUNT(*) AS jobs
    FROM jobs
    WHERE salary_min IS NOT NULL
    GROUP BY search_query
    ORDER BY avg_salary DESC
""")

run("Postings per day", """
    SELECT posted_date, COUNT(*) AS jobs
    FROM jobs
    GROUP BY posted_date
    ORDER BY posted_date
""")

run("Old postings check", """
    SELECT title, company, posted_date
    FROM jobs
    WHERE posted_date < '2022-01-01'
    ORDER BY posted_date
""")

run("Missing data check", """
    SELECT
        COUNT(*)                              AS total,
        SUM(salary_min IS NOT NULL)           AS with_salary,
        SUM(company IS NULL OR company = '')  AS missing_company,
        SUM(state IS NULL)                    AS missing_state
    FROM jobs
""")

conn.close()