import asyncio
import sys
from loguru import logger
from CORE.bot import bot
from CORE.dispatcher import dp
from CORE.config import settings
from DATABASE.base import init_db
from SERVICES.utils.scheduler import setup_scheduler, shutdown_scheduler

# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)

async def on_startup():
    """Действия при запуске бота"""
    logger.info("🚀 Запуск TrixBot♥️ - Будапешт")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Инициализация БД
    await init_db()
    logger.info("✅ База данных инициализирована")
    
    # Регистрация middleware
    from HANDLERS.special.middleware import LoggingMiddleware, ThrottlingMiddleware, UserTrackingMiddleware
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(UserTrackingMiddleware())
    logger.info("✅ Middleware зарегистрированы")
    
    # Регистрация обработчика ошибок
    from HANDLERS.special.errors import router as error_router
    from HANDLERS.callbacks.rating_callbacks import router as rating_callback_router
    dp.include_router(error_router)
    dp.include_router(rating_callback_router)
    logger.info("✅ Error handler и callbacks зарегистрированы")
    
    # Запуск планировщика
    setup_scheduler()
    
    # Проверка подключения
    me = await bot.get_me()
    logger.info(f"✅ Бот запущен: @{me.username}")
    logger.info(f"Bot ID: {me.id}")

async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("🛑 Остановка TrixBot♥️")
    shutdown_scheduler()
    await bot.session.close()

async def main():
    """Основная функция"""
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        logger.info("📡 Начинаю polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.exception(f"❌ Критическая ошибка: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Бот остановлен пользователем")
