"""
Настройка диспетчера и регистрация обработчиков
"""
from aiogram import Dispatcher
from loguru import logger

# Импорты обработчиков
from handlers.commands import (
    start_handler,
    help_handler,
    catalog_handler,
    rating_handler,
    admin_handler
)
from handlers.callbacks import (
    catalog_callbacks,
    rating_callbacks,
    admin_callbacks
)
from handlers.messages import (
    catalog_messages,
    rating_messages
)
from middleware import (
    logging_middleware,
    throttling_middleware,
    user_middleware
)


def setup_dispatcher() -> Dispatcher:
    """Создание и настройка диспетчера"""
    dp = Dispatcher()
    
    # Регистрация middleware
    dp.message.middleware(logging_middleware.LoggingMiddleware())
    dp.message.middleware(throttling_middleware.ThrottlingMiddleware())
    dp.message.middleware(user_middleware.UserTrackingMiddleware())
    dp.callback_query.middleware(logging_middleware.LoggingMiddleware())
    
    # Регистрация обработчиков команд
    dp.include_router(start_handler.router)
    dp.include_router(help_handler.router)
    dp.include_router(catalog_handler.router)
    dp.include_router(rating_handler.router)
    dp.include_router(admin_handler.router)
    
    # Регистрация обработчиков callback
    dp.include_router(catalog_callbacks.router)
    dp.include_router(rating_callbacks.router)
    dp.include_router(admin_callbacks.router)
    
    # Регистрация обработчиков сообщений
    dp.include_router(catalog_messages.router)
    dp.include_router(rating_messages.router)
    
    logger.info("✅ Диспетчер настроен с обработчиками")
    return dp
