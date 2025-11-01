"""
Главная точка входа в бот
TrixBot♥️ - Будапешт @Trixlivebot
"""
import asyncio
import sys
from loguru import logger

from telegram.ext import Application
from CORE.config import settings


# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)
logger.add(
    "logs/bot_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    level="INFO"
)


async def init_database():
    """Безопасная инициализация базы данных"""
    try:
        from DATABASE.base import init_db
        db_success = await init_db()
        if db_success:
            logger.info("✅ База данных готова")
            return True
        else:
            logger.warning("⚠️ База данных не инициализирована")
            return False
    except Exception as e:
        if "already exists" in str(e):
            logger.info("✅ Таблицы уже существуют")
            return True
        else:
            logger.error(f"❌ Ошибка инициализации БД: {e}")
            return False


async def main():
    """Главная функция запуска бота"""
    # Инициализация базы данных (ТОЛЬКО ОДИН РАЗ)
    db_ready = await init_database()
    if not db_ready:
        logger.warning("⚠️ Продолжаем без базы данных")

    # Создаем приложение бота
    application = Application.builder().token(settings.BOT_TOKEN).build()
    
    # TODO: Регистрируем handlers здесь
    # from HANDLERS import register_handlers
    # register_handlers(application)
    
    # Запускаем бота
    try:
        logger.info("🚀 Запуск TrixBot♥️ - Будапешт")
        
        # Получаем информацию о боте
        bot_info = await application.bot.get_me()
        logger.info(f"✅ Бот запущен: @{bot_info.username} (ID: {bot_info.id})")
        logger.info(f"📍 Режим: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
        
        await application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"],
            timeout=30,
            pool_timeout=30
        )
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
