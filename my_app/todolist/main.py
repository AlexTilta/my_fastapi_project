from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title='ToDo-Service')

class Task(BaseModel):
    title:str
    description: str = None
    completed: bool = False

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        completed BOOLEAN
    )
""")

task_id_counter = 1

# Создание новой задачи
@app.post('/items')
def create_task(task: Task):
    global task_id_counter
    cur.execute(
        "INSERT INTO tasks (task_id, title, description, completed) VALUES (?, ?, ?, ?)",
        (task_id_counter, task.title, task.description, task.completed)
    )
    conn.commit()
    task_id_counter += 1
    return {"task_id": task_id_counter - 1, "task": task.title, "task_description": task.description, "status": task.completed}

# Получение списка всех задач
@app.get('/items')
def get_all_tasks():
    cur.execute("SELECT * FROM tasks;")

    tasks = cur.fetchall()
    return {"tasks": tasks}

# Получение задачи по ID
@app.get('/items/{item_id}')
def get_task(item_id: int):
    cur.execute("SELECT title, description, completed FROM tasks WHERE task_id=?", (item_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    title, description, status = row[0], row[1], row[2]
    return {"task_id": item_id, "task": title, "description": description, "status": status}

# Обновление задачи по ID
@app.put('/items/{item_id}')
def update_task(item_id: int, updated_task: Task):
    cur.execute("SELECT title FROM tasks WHERE task_id=?", (item_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    cur.execute(
        "UPDATE tasks SET description = ?, completed = ? WHERE task_id = ?",
        (updated_task.description, updated_task.completed, item_id)
    )
    conn.commit()
    return {"id": item_id, "task": updated_task.title, "task_description": updated_task.description}

# Удаление задачи по ID
@app.delete('/items/{item_id}')
def delete_task(item_id: int):
    cur.execute("SELECT title FROM tasks WHERE task_id=?", (item_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    cur.execute("DELETE FROM tasks WHERE task_id = ?", (item_id,))
    conn.commit()
    return {"id": item_id, "status": "deleted"}