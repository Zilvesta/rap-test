from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TimestampData(BaseModel):
    video_id: str
    timestamp: int

DB_FILE = "timestamps.db"
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS timestamps (video_id TEXT, timestamp INTEGER)")
    conn.commit()
    conn.close()

@app.get("/")
def read_root():
    return {"message": "Rap Test Backend is running"}

@app.post("/timestamps")
def save_timestamp(data: TimestampData):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO timestamps (video_id, timestamp) VALUES (?, ?)", (data.video_id, data.timestamp))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.get("/timestamps/{video_id}")
def get_timestamps(video_id: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp FROM timestamps WHERE video_id=?", (video_id,))
    results = c.fetchall()
    conn.close()
    return {"timestamps": [r[0] for r in results]}

if not os.path.exists("video_player"):
    os.makedirs("video_player")

app.mount("/static", StaticFiles(directory="video_player", html=True), name="static")
