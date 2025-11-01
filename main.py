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


async def main():
    """Основная функция бота"""
    try:
        logger.info("✅ Используем существующие таблицы БД")
        
        # Создаем приложение бота
        application = Application.builder().token(settings.BOT_TOKEN).build()
        
        # TODO: Регистрируем handlers здесь
        # from HANDLERS import register_handlers
        # register_handlers(application)
        
        # Получаем информацию о боте
        bot_info = await application.bot.get_me()
        logger.info(f"✅ Бот запущен: @{bot_info.username} (ID: {bot_info.id})")
        logger.info(f"📍 Режим: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
        
        logger.info("🚀 Запуск TrixBot♥️ - Будапешт")
        
        # Простой запуск polling
        await application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        
    except asyncio.CancelledError:
        logger.info("🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка при работе бота: {e}")
        raise


if __name__ == "__main__":
    try:
        # Простой и надежный запуск
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
