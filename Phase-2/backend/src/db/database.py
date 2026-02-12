"""
Database connection and session management
Supports both SQLite (development) and PostgreSQL (production)
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment - default to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./todo.db"
)

# Handle PostgreSQL URL for Neon
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove unsupported query parameters for asyncpg
if "asyncpg" in DATABASE_URL and ("sslmode=" in DATABASE_URL or "channel_binding=" in DATABASE_URL):
    if "?" in DATABASE_URL:
        base_url, query = DATABASE_URL.split("?", 1)
        params = [p for p in query.split("&") if not p.startswith(("sslmode=", "channel_binding="))]
        DATABASE_URL = base_url + ("?" + "&".join(params) if params else "")

# Determine if using Neon PostgreSQL
is_neon = "neon.tech" in DATABASE_URL

# Create async engine with appropriate settings
if "sqlite" in DATABASE_URL:
    # SQLite configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        future=True,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        future=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"ssl": "require"} if is_neon else {},
    )

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connection"""
    await engine.dispose()
