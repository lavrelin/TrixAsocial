"""
Базовые модели и настройка БД
"""
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from loguru import logger

from CORE.config import settings


# Базовый класс для моделей
class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


# Общие миксины
class TimestampMixin:
    """Миксин для автоматических временных меток"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


# Создание движка БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        # Импортируем все модели перед создани ем таблиц
        from DATABASE import users, catalog, games, posts, analytics
        
        # Создаем таблицы
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Таблицы базы данных созданы")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
