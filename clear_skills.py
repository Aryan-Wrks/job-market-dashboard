import sqlite3
conn = sqlite3.connect("jobs.db")
conn.execute("DELETE FROM skills")
conn.commit()
conn.close()
print("Cleared old skills, ready to re-extract")