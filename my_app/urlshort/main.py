from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI(title='Short_URL')

class URLItem(BaseModel):
    url: str

conn = sqlite3.connect("urlshort/urls.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        short_id TEXT PRIMARY KEY,
        full_url TEXT NOT NULL
    )
""")

conn.commit()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        cur.execute("SELECT 1 FROM urls WHERE short_id = ?", (short_id,))
        if cur.fetchone() is None:
            return short_id
        
# Создание короткой ссылки взамен длинного URL
@app.post('/shorten')
def generate_short_url(item: URLItem):
    short_id = generate_short_id()
    cur.execute(
        "INSERT INTO urls (short_id, full_url) VALUES (?, ?)",
        (short_id, item.url)
    )
    conn.commit()
    return {"short_url": f"https://127.0.0.1:8000/{short_id}"}

# Перенаправление на первоначальный URL по короткому ID
@app.get('/{short_id}')
def redirected_to_url(short_id: str):
    cur.execute("SELECT full_url FROM urls WHERE short_id=?", (short_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="URL not found")
    full_url = row[0]
    return RedirectResponse(full_url)

# Получаем информацию о полном URL на основе ID
@app.get('/stats/{short_id}')
def info_about_url(short_id: str):
    cur.execute("SELECT full_url FROM urls WHERE short_id=?", (short_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="URL not found")
    full_url = row[0]
    return {"short_id": short_id, "full_url": full_url}