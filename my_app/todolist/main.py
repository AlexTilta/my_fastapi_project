from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title='ToDo-Service')

class Task(BaseModel):
    title:str
    description: str = None
    completed: bool = False

conn = sqlite3.connect("todolist/tasks.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        title TEXT PRIMARY KEY,
        description TEXT NOT NULL,
        completed BOOL
    )
""")

task_id_counter = 1

# Создание новой задачи
@app.post('/items')
def create_task(task: Task):
    global task_id_counter
    tasks[task_id_counter] = task.title
    task_id_counter += 1
    return {"id": task_id_counter - 1, "task": task.title, "task_description": task.description}

# Получение списка всех задач
@app.get('/items')
def get_all_tasks():
    return {"tasks": tasks}

# Получение задачи по ID
@app.get('/items/{item_id}')
def get_task(item_id: int):
    if item_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    return tasks[item_id]

# Обновление задачи по ID
@app.put('/items/{item_id}')
def update_task(item_id: int, updated_task: Task):
    if item_id not in tasks:
        raise HTTPException(status_code=404, detail='Task for update not found')
    tasks[item_id] = update_task.title
    return {"id": item_id, "task": update_task.title, "task_description": update_task.description}

# Удаление задачи по ID
@app.delete('/items/{item_id}')
def delete_task(item_id: int):
    if item_id not in tasks:
        raise HTTPException(status_code=404, detail='Task for delete not found')
    del tasks[item_id]
    return {"id": item_id, "status": "deleted"}