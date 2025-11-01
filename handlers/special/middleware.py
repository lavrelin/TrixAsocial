from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from loguru import logger
from datetime import datetime

class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех сообщений"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user = event.from_user
            logger.info(
                f"📨 Message from @{user.username} (ID:{user.id}): {event.text[:50] if event.text else '[Media]'}"
            )
        
        return await handler(event, data)

class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для защиты от флуда"""
    
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.user_last_message: Dict[int, datetime] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user_id = event.from_user.id
            now = datetime.now()
            
            if user_id in self.user_last_message:
                time_passed = (now - self.user_last_message[user_id]).total_seconds()
                
                if time_passed < self.rate_limit:
                    logger.warning(f"⚠️ Throttling user {user_id}")
                    await event.answer("⏰ Не так быстро! Подождите немного.")
                    return
            
            self.user_last_message[user_id] = now
        
        return await handler(event, data)

class UserTrackingMiddleware(BaseMiddleware):
    """Middleware для отслеживания активности пользователей"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            from DATABASE.base import get_session
            from SERVICES.database.user_service import UserService
            
            async for session in get_session():
                user = await UserService.get_or_create_user(
                    session=session,
                    user_id=event.from_user.id,
                    username=event.from_user.username,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name,
                    language_code=event.from_user.language_code
                )
                
                # Обновляем активность
                user.last_activity = datetime.utcnow()
                user.message_count += 1
                await session.commit()
        
        return await handler(event, data)
