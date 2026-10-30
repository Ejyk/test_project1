# check_columns.py
import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("PRAGMA table_info(artisans)")
columns = c.fetchall()

for col in columns:
    print(col)

conn.close()
