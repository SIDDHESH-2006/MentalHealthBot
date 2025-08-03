# routes/user_routes.py

import sqlite3
from fastapi import APIRouter, HTTPException
from models.user import UserCreate, LoginInput

DB_PATH = "user_db.sqlite3"

def init_user_db():
    """
    Create the users table in user_db.sqlite3 if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the user DB on module import
init_user_db()

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register")
def register(user: UserCreate):
    """
    Registers a new user. Fails if the email is already taken.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (user.name, user.email, user.password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")
    conn.close()
    return {"msg": "User registered"}


@router.post("/login")
def login(credentials: LoginInput):
    """
    Authenticates a user by email and password.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT name, password FROM users WHERE email = ?",
        (credentials.email,)
    )
    row = c.fetchone()
    conn.close()

    if row is None or row[1] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid login")

    return {"msg": "Login successful", "name": row[0]}
