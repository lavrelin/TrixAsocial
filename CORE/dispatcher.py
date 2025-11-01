"""
Настройка диспетчера и регистрация обработчиков
"""
from aiogram import Dispatcher
from loguru import logger

# Импорты обработчиков
from HANDLERS.commands import start, help, menu, admin_commands


def setup_dispatcher() -> Dispatcher:
    """Создание и настройка диспетчера"""
    dp = Dispatcher()
    
    # Регистрация middleware
    # TODO: Добавить middleware для логирования, антифлуд и т.д.
    
    # Регистрация обработчиков команд
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(admin_commands.router)
    
    # TODO: Регистрация остальных обработчиков (callbacks, messages, special)
    
    logger.info("✅ Диспетчер настроен с обработчиками")
    return dp


# Создаем экземпляр диспетчера
dp = setup_dispatcher()
