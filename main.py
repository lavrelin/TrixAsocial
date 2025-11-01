"""
Главная точка входа в бот
TrixBot♥️ - Будапешт @Trixlivebot
"""
import asyncio
import sys
from loguru import logger

from CORE.bot import bot
from CORE.dispatcher import dp
from CORE.config import settings
from DATABASE.base import init_db


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


async def on_startup():
    """Действия при запуске бота"""
    logger.info("🚀 Запуск TrixBot♥️ - Будапешт")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Инициализация базы данных
    await init_db()
    logger.info("✅ База данных инициализирована")
    
    # Проверка подключения
    me = await bot.get_me()
    logger.info(f"✅ Бот запущен: @{me.username}")
    logger.info(f"Bot ID: {me.id}")


async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("🛑 Остановка TrixBot♥️")
    await bot.session.close()


# main.py
async def main():
    # Инициализация базы данных
    try:
        from DATABASE.base import init_db
        db_success = await init_db()
        if db_success:
            logger.info("✅ База данных готова")
        else:
            logger.warning("⚠️ База данных не инициализирована, продолжаем в ограниченном режиме")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        logger.warning("⚠️ Продолжаем без базы данных")

    # Создаем приложение бота
    application = Application.builder().token(settings.BOT_TOKEN).build()
    
    # Регистрируем handlers...
    
    # Запускаем бота
    try:
        logger.info("🚀 Запуск бота...")
        await application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"],
            timeout=30
        )
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
