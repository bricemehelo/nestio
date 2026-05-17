# app/database.py
#
# PURPOSE: Establishes the PostgreSQL database connection for the entire application.
# This file is the single source of truth for database connectivity.
#
# PATTERN: Singleton — the engine and session factory are created ONCE at startup
# and reused across all requests. SQLAlchemy manages the connection pool internally,
# so we don't open a new physical connection per request — just borrow one from the pool.
#
# SQLAlchemy ROLE: Acts as the ORM (Object Relational Mapper). It translates Python
# class definitions into database tables, and Python method calls into SQL queries.
# We never write raw SQL — SQLAlchemy handles that translation layer.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file
# This ensures DATABASE_URL never appears hardcoded in source code (OWASP: secure config)
load_dotenv()

# Read the database connection string from environment
# Format: postgresql://username:password@host:port/database_name
# Example: postgresql://brice:secret@localhost:5432/nestio_db
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fail loudly at startup — a missing DB URL is a fatal misconfiguration.
    # Better to crash immediately with a clear message than to fail silently later.
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file.")

# Create the SQLAlchemy engine — the Singleton.
# The engine manages the connection pool and knows which DB dialect to use (PostgreSQL here).
#
# pool_pre_ping=True — before handing a connection from the pool to a request,
# SQLAlchemy tests it with a lightweight "ping". If the connection dropped (e.g. DB restarted),
# it will reconnect automatically instead of crashing with a stale connection error.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory for creating database sessions.
# Each request will call SessionLocal() to get its own session — used to run queries,
# then closed at the end of the request. Sessions are NOT shared between requests.
#
# autocommit=False — we control when transactions are committed (explicit is safer)
# autoflush=False — SQLAlchemy won't auto-push changes to DB mid-session (we control this)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all SQLAlchemy models (e.g. Property).
# When a model inherits from Base, SQLAlchemy registers it and knows how to
# map that Python class to a PostgreSQL table.
class Base(DeclarativeBase):
    pass

# get_db is a FastAPI dependency — it will be injected into route handlers
# that need database access (via the Repository layer, not directly in routes).
#
# Using Python's yield turns this into a context manager:
# - Before yield: creates and opens a session for the request
# - After yield: closes the session (in the finally block — always runs, even on errors)
#
# FastAPI's dependency injection calls this automatically per request.
def get_db():
    db = SessionLocal()
    try:
        yield db  # The session is passed to whoever needs it (the repository)
    finally:
        db.close()  # Always close — prevents connection leaks

# Import all models here so SQLAlchemy's Base is aware of them
# Alembic reads Base.metadata to detect tables — models must be imported first
from app.models import property  # noqa: F401