# alembic/env.py
#
# PURPOSE: Configures Alembic to use our SQLAlchemy models and .env DATABASE_URL.
# This file is the bridge between Alembic and our FastAPI application.

import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load .env so DATABASE_URL is available
load_dotenv()

# Import Base from our app so Alembic can detect all registered models
# This is how Alembic knows what tables to create or modify
from app.database import Base

# Import all models so they register themselves on Base.metadata
# Without this import, Alembic sees an empty Base and generates no migrations
from app.models import property  # noqa: F401

# Alembic Config object — gives access to alembic.ini values
config = context.config

# Set the database URL dynamically from environment — never hardcoded
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Set up logging from alembic.ini configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata tells Alembic to compare against our SQLAlchemy models
# This enables --autogenerate to detect what changed
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without a live DB connection — generates SQL scripts only."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live DB connection — applies changes directly."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()