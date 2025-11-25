from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from app.core.config import settings

# Determine database type and create appropriate engine
if settings.DATABASE_URL.startswith('sqlite'):
    # SQLite configuration for development
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Better for SQLite with FastAPI
        echo=False  # Set to True to see SQL queries in logs
    )
else:
    # PostgreSQL/other databases
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency to get database session
    Usage: 
        def some_endpoint(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables (for testing)"""
    Base.metadata.drop_all(bind=engine)

def check_database_health() -> bool:
    """Check if database is accessible"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

def get_database_info() -> dict:
    """Get database information"""
    return {
        "url": settings.DATABASE_URL,
        "dialect": engine.dialect.name,
        "tables": list(Base.metadata.tables.keys()),
        "healthy": check_database_health()
    }