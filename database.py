from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import environ
from urllib.parse import quote_plus

DATABASE_URL = environ.get('DB_URL')

import os

password = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL = f"postgresql+asyncpg://events_user:{password}@postgres:5432/events_db"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

