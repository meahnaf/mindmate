from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL - using SQLite file 'journal.db'
DATABASE_URL = "sqlite:///./journal.db"

# Engine connects SQLAlchemy to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for interacting with DB
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for model declarations
Base = declarative_base()

# Our table model
class JournalEntry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
