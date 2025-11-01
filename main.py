"""
TrixBot♥️ - Main Entry Point
"""
import asyncio
from loguru import logger

from CORE.bot import bot
from CORE.dispatcher import dp  
from DATABASE.base import init_db
from SERVICES.utils.scheduler import setup_scheduler, shutdown_scheduler


async def main():
    """Главная функция"""
    logger.info("🚀 Запуск TrixBot...")
    
    try:
        await init_db()
        setup_scheduler()
        
        me = await bot.get_me()
        logger.success(f"✅ Бот запущен: @{me.username}")
        
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.exception(f"❌ Ошибка: {e}")
    finally:
        shutdown_scheduler()


if __name__ == "__main__":
    asyncio.run(main())
