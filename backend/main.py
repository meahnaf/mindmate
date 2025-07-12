from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ========== Database Setup ==========
DATABASE_URL = "sqlite:///./journal.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# ========== Entry Model ==========
class JournalEntry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ========== Pydantic Schemas ==========
class EntryCreate(BaseModel):
    title: str
    content: str

class EntryOut(BaseModel):
    id: int
    title: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

# ========== FastAPI App ==========
app = FastAPI()

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== API Routes ==========

# Add new entry
@app.post("/add")
def add_entry(entry: EntryCreate):
    new_entry = JournalEntry(title=entry.title, content=entry.content)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Entry added successfully!"}

# Get all entries
@app.get("/entries", response_model=List[EntryOut])
def get_entries():
    return db.query(JournalEntry).all()

# Delete an entry
@app.delete("/entry/{entry_id}")
def delete_entry(entry_id: int):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}

# Edit/Update an entry
@app.put("/entry/{entry_id}")
def update_entry(entry_id: int, updated: EntryCreate):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    entry.title = updated.title
    entry.content = updated.content
    db.commit()
    return {"message": "Entry updated successfully"}
