import sqlite3

conn = sqlite3.connect("todolist/tasks.db")
cur = conn.cursor()

cur.execute("SELECT * FROM tasks;")

rows = cur.fetchall()

for row in rows:
    print({"task_id": row[0], "title": row[1], "description": row[2], "status": row[3]})