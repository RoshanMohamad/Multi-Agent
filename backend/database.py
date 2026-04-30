from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Default to SQLite for local development
# In production, change this via environment variable to your RDS PostgreSQL string
# Example: "postgresql://user:password@rds-endpoint.amazonaws.com/dbname"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./multi_agent.db")

# SQLite requires this flag, standard Postgres does not
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True, default="anonymous")
    agent_id = Column(String(50), index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Automatically create tables. In a true production app, use Alembic for migrations.
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
