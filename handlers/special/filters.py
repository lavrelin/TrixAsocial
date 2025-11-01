from aiogram.filters import Filter
from aiogram.types import Message
from CORE.config import settings

class IsAdminFilter(Filter):
    """Фильтр для проверки прав администратора"""
    
    async def __call__(self, message: Message) -> bool:
        return settings.is_admin(message.from_user.id)

class IsChannelFilter(Filter):
    """Фильтр для проверки что сообщение из канала"""
    
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.id == self.channel_id

class HasMediaFilter(Filter):
    """Фильтр для проверки наличия медиа"""
    
    async def __call__(self, message: Message) -> bool:
        return bool(message.photo or message.video or message.document or message.animation)
