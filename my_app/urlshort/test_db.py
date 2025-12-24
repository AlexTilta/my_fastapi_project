import sqlite3

conn = sqlite3.connect("urlshort/urls.db")
cur = conn.cursor()

cur.execute("SELECT * FROM urls;")

rows = cur.fetchall()

for row in rows:
    print({"short_id": row[0], "full_url": row[1]})