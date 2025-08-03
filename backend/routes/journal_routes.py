# routes/journal_routes.py

import sqlite3
from fastapi import APIRouter, HTTPException
from models.journal import EntryInput
from services.emotion_detector import analyze_emotion
from datetime import datetime

DB_PATH = "journal_db.sqlite3"

def init_journal_db():
    """
    Create the journal_entries table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            emotion TEXT NOT NULL,
            sentiment REAL NOT NULL,
            transcription TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the journal DB on module import
init_journal_db()

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.post("/entry")
def add_entry(user_email: str, entry: EntryInput):
    """
    Analyze emotion, save a new journal entry to SQLite, and return the results.
    """
    # 1) Run your AI emotion analysis
    emotion, sentiment = analyze_emotion(entry.text)

    # 2) Use provided timestamp or now
    ts = entry.timestamp or datetime.utcnow().isoformat()

    # 3) Insert into the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO journal_entries 
          (user_email, text, timestamp, emotion, sentiment, transcription)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_email, entry.text, ts, emotion, sentiment, entry.transcription)
    )
    conn.commit()
    conn.close()

    return {"msg": "Entry saved", "emotion": emotion, "sentiment": sentiment}


@router.get("/history", response_model=List[dict])
def get_entries(user_email: str):
    """
    Retrieve all journal entries for a given user_email.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT text, timestamp, emotion, sentiment, transcription "
        "FROM journal_entries WHERE user_email = ?",
        (user_email,)
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No entries found for this user")

    # Convert sqlite3.Row objects to plain dicts
    entries = [dict(row) for row in rows]
    return entries
