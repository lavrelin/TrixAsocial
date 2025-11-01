"""
Базовые модели и настройка БД
"""
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import BigInteger, DateTime, func, text
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


async def table_exists(table_name: str) -> bool:
    """Проверяет существование таблицы в базе данных"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name)"),
                {"table_name": table_name}
            )
            exists = result.scalar()
            logger.debug(f"Таблица {table_name} существует: {exists}")
            return exists
    except Exception as e:
        logger.warning(f"Ошибка проверки таблицы {table_name}: {e}")
        return False


async def safe_create_tables():
    """Безопасное создание таблиц с проверкой существования"""
    try:
        # Импортируем все модели перед созданием таблиц
        from DATABASE import users, catalog, games, posts, analytics
        
        # Проверяем основные таблицы
        tables_to_check = ['users', 'catalog_posts', 'catalog_reviews', 'rating_posts']
        
        all_tables_exist = True
        for table in tables_to_check:
            if not await table_exists(table):
                all_tables_exist = False
                break
        
        if all_tables_exist:
            logger.info("✅ Все таблицы уже существуют")
            return True
        
        # Создаем таблицы если какие-то отсутствуют
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Таблицы базы данных созданы")
            return True
            
    except Exception as e:
        if "already exists" in str(e):
            logger.info("✅ Таблицы уже существуют (перехвачена ошибка)")
            return True
        else:
            logger.error(f"❌ Ошибка создания таблиц: {e}")
            return False


async def init_db():
    """Инициализация базы данных"""
    success = await safe_create_tables()
    if not success:
        logger.warning("⚠️ Продолжаем без полной инициализации БД")
    return success


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Ошибка сессии БД: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
