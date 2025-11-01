"""
Главная точка входа в бот
TrixBot♥️ - Будапешт @Trixlivebot
"""
import asyncio
import sys
import signal
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


class BotRunner:
    def __init__(self):
        self.application = None
        self.shutdown_event = asyncio.Event()

    async def setup(self):
        """Настройка приложения бота"""
        try:
            # Инициализация базы данных
            logger.info("✅ Используем существующие таблицы БД")
            
            # Создаем приложение бота
            self.application = Application.builder().token(settings.BOT_TOKEN).build()
            
            # TODO: Регистрируем handlers здесь
            # from HANDLERS import register_handlers
            # register_handlers(application)
            
            logger.info("🚀 TrixBot♥️ - Будапешт инициализирован")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки бота: {e}")
            return False

    async def run(self):
        """Запуск бота"""
        if not self.application:
            logger.error("❌ Приложение бота не инициализировано")
            return

        try:
            # Получаем информацию о боте
            bot_info = await self.application.bot.get_me()
            logger.info(f"✅ Бот запущен: @{bot_info.username} (ID: {bot_info.id})")
            logger.info(f"📍 Режим: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
            
            # Запускаем polling с правильными параметрами
            await self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"],
                close_loop=False  # Важно: не закрывать loop
            )
            
        except asyncio.CancelledError:
            logger.info("🛑 Получен сигнал остановки")
        except Exception as e:
            logger.error(f"❌ Ошибка при работе бота: {e}")
            raise

    async def shutdown(self):
        """Корректное завершение работы бота"""
        if self.application:
            logger.info("🛑 Остановка бота...")
            try:
                await self.application.stop()
                await self.application.shutdown()
                logger.info("✅ Бот корректно остановлен")
            except Exception as e:
                logger.error(f"❌ Ошибка при остановке бота: {e}")


def handle_signal(runner):
    """Обработчик сигналов для graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"📡 Получен сигнал {signum}, завершение работы...")
        runner.shutdown_event.set()
        
    signal.signal(signal.SIGINT, lambda s, f: handle_signal(runner)(s, f))
    signal.signal(signal.SIGTERM, lambda s, f: handle_signal(runner)(s, f))


async def main_async():
    """Основная асинхронная функция"""
    runner = BotRunner()
    
    # Настройка обработчиков сигналов
    handle_signal(runner)
    
    try:
        # Инициализация бота
        if not await runner.setup():
            logger.error("❌ Не удалось инициализировать бота")
            return 1

        # Запуск бота в отдельной задаче
        bot_task = asyncio.create_task(runner.run())
        
        # Ожидание сигнала завершения или ошибки
        await asyncio.wait(
            [bot_task, asyncio.create_task(runner.shutdown_event.wait())],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Если бот еще работает, останавливаем его
        if not bot_task.done():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
        
        # Корректное завершение
        await runner.shutdown()
        return 0
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        await runner.shutdown()
        return 1


def main():
    """Главная функция запуска"""
    try:
        # Устанавливаем политику event loop для Unix систем
        if sys.platform != 'win32':
            try:
                import uvloop
                uvloop.install()
                logger.debug("✅ Используется uvloop")
            except ImportError:
                logger.debug("ℹ️  uvloop не установлен, используется стандартный asyncio")
        
        # Запускаем асинхронную главную функцию
        exit_code = asyncio.run(main_async())
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
