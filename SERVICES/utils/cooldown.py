from datetime import datetime, timedelta
from typing import Tuple
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from DATABASE.games import Cooldown
from CORE.config import settings

class CooldownService:
    """Сервис управления кулдаунами"""
    
    @staticmethod
    async def check_cooldown(
        session: AsyncSession,
        user_id: int,
        command: str
    ) -> Tuple[bool, int]:
        """
        Проверить кулдаун команды
        Возвращает (можно_использовать, секунд_осталось)
        """
        # Удаляем истекшие кулдауны
        await session.execute(
            delete(Cooldown).where(Cooldown.expires_at < datetime.utcnow())
        )
        await session.commit()
        
        # Проверяем текущий кулдаун
        result = await session.execute(
            select(Cooldown).where(
                Cooldown.user_id == user_id,
                Cooldown.command == command
            )
        )
        cooldown = result.scalar_one_or_none()
        
        if not cooldown:
            return True, 0
        
        time_left = int((cooldown.expires_at - datetime.utcnow()).total_seconds())
        
        if time_left <= 0:
            # Кулдаун истек, удаляем
            await session.delete(cooldown)
            await session.commit()
            return True, 0
        
        return False, time_left
    
    @staticmethod
    async def set_cooldown(
        session: AsyncSession,
        user_id: int,
        command: str
    ):
        """Установить кулдаун для команды"""
        # Определяем длительность
        duration_map = {
            'gorateme': settings.GORATEME_COOLDOWN,
            'review': settings.REVIEW_COOLDOWN
        }
        duration = duration_map.get(command, 3600)  # По умолчанию 1 час
        
        # Удаляем старый кулдаун если есть
        await session.execute(
            delete(Cooldown).where(
                Cooldown.user_id == user_id,
                Cooldown.command == command
            )
        )
        
        # Создаем новый
        cooldown = Cooldown(
            user_id=user_id,
            command=command,
            expires_at=datetime.utcnow() + timedelta(seconds=duration)
        )
        session.add(cooldown)
        await session.commit()
