# routes/auth_routes.py

import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

DB_PATH = "auth_db.sqlite3"

def init_auth_db():
    """
    Create the users table in auth_db.sqlite3 if it doesn't exist.
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

# Initialize the database on module import
init_auth_db()

router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupInput(BaseModel):
    name: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignupInput):
    """
    Register a new user. Fails if the email is already in use.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (data.name, data.email, data.password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    conn.close()
    return {"message": "Signup successful", "name": data.name}


@router.post("/login")
def login(data: LoginInput):
    """
    Authenticate a user by email and password.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT name, password FROM users WHERE email = ?",
        (data.email,)
    )
    row = c.fetchone()
    conn.close()

    if row is None or row[1] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "name": row[0]}
