from fastapi import APIRouter
import sqlite3

def init_db():
    conn = sqlite3.connect("journal_db.sqlite3")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_text TEXT,
            ai_response TEXT
        )
    """)
    conn.commit()
    conn.close()

router = APIRouter()

@router.get("/analytics/mood_trends")
def get_mood_trends(user_email: str):
    # Connect to the SQLite database
    conn = sqlite3.connect("journal_db.sqlite3")
    conn.row_factory = sqlite3.Row  # So we can use row["column_name"]
    c = conn.cursor()

    # Get relevant entries from the DB (filter logic can be customized)
    c.execute("""
        SELECT timestamp, ai_response 
        FROM journal_entries 
        WHERE user_text LIKE ?
    """, (f"%{user_email}%",))  # Example way to link entries to a user

    rows = c.fetchall()
    conn.close()

    # Extract dummy mood/sentiment (replace later with real parsing from ai_response)
    dates, moods, scores = [], [], []
    for row in rows:
        dates.append(row["timestamp"][:10])
        moods.append("neutral")      # <-- You can parse real mood from ai_response later
        scores.append(0.5)           # <-- Placeholder score

    return {
        "dates": dates,
        "moods": moods,
        "sentiment_score": scores
    }
