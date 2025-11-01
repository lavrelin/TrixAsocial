"""
Health check для Railway
"""
import asyncio
from loguru import logger

from CORE.bot import bot
from DATABASE.base import engine


async def check_bot():
    """Проверка работы бота"""
    try:
        me = await bot.get_me()
        logger.info(f"✅ Bot OK: @{me.username}")
        return True
    except Exception as e:
        logger.error(f"❌ Bot check failed: {e}")
        return False


async def check_database():
    """Проверка подключения к БД"""
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info("✅ Database OK")
        return True
    except Exception as e:
        logger.error(f"❌ Database check failed: {e}")
        return False


async def health_check():
    """Полная проверка здоровья системы"""
    bot_ok = await check_bot()
    db_ok = await check_database()
    
    if bot_ok and db_ok:
        logger.info("✅ Health check passed")
        return True
    else:
        logger.error("❌ Health check failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(health_check())
    exit(0 if result else 1)
