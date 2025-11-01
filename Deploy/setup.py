"""
Скрипт первоначальной настройки
"""
import asyncio
from loguru import logger

from DATABASE.base import init_db, engine
from CORE.config import settings


async def setup():
    """Первоначальная настройка"""
    logger.info("🚀 Начало настройки...")
    
    # Проверка конфигурации
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL[:30]}...")
    
    # Инициализация БД
    try:
        await init_db()
        logger.info("✅ База данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        return False
    
    logger.info("✅ Настройка завершена успешно")
    return True


if __name__ == "__main__":
    result = asyncio.run(setup())
    exit(0 if result else 1)
