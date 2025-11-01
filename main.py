"""
TrixBot - главная точка входа
Инициализация и запуск бота
"""
import asyncio
import logging
from loguru import logger

from core.bot import bot
from core.dispatcher import setup_dispatcher
from database.base import init_db
from services.scheduler import setup_scheduler, shutdown_scheduler


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger.add("logs/trixbot.log", rotation="1 day", retention="7 days", level="INFO")


async def on_startup():
    """Действия при запуске бота"""
    logger.info("🚀 Запуск TrixBot...")
    
    # Инициализация базы данных
    success = await init_db()
    if not success:
        logger.error("❌ Не удалось инициализировать базу данных")
        return False
    
    # Настройка планировщика задач
    setup_scheduler()
    
    # Получение информации о боте
    bot_info = await bot.get_me()
    logger.success(f"✅ Бот запущен: @{bot_info.username} (ID: {bot_info.id})")
    
    return True


async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("🛑 Остановка бота...")
    
    # Остановка планировщика
    shutdown_scheduler()
    
    # Закрытие сессии бота
    await bot.session.close()
    
    logger.info("👋 Бот остановлен")


async def main():
    """Главная функция запуска"""
    try:
        # Действия при запуске
        success = await on_startup()
        if not success:
            logger.error("❌ Не удалось запустить бота")
            return
        
        # Настройка диспетчера
        dp = setup_dispatcher()
        
        # Запуск поллинга
        logger.info("📡 Запуск polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.exception(f"❌ Критическая ошибка: {e}")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚡ Бот остановлен пользователем")
    except Exception as e:
        logger.exception(f"❌ Неожиданная ошибка: {e}")
