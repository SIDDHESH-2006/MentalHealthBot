from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3

class EntryInput(BaseModel):
    text: str
    timestamp: Optional[datetime] = None
    transcription: Optional[str] = None

class EntryResponse(BaseModel):
    date: str
    text: str
    emotion: str
    sentiment: float