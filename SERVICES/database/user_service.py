import random
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from DATABASE.users import User
from CORE.config import settings

class UserService:
    @staticmethod
    async def generate_unique_uid(session: AsyncSession) -> int:
        available_uids = set(range(settings.MIN_UID, settings.MAX_UID + 1))
        available_uids -= set(settings.RESERVED_UIDS)
        
        result = await session.execute(select(User.uid))
        used_uids = {row[0] for row in result.all()}
        available_uids -= used_uids
        
        if not available_uids:
            raise ValueError("Нет доступных UID!")
        
        return random.choice(list(available_uids))
    
    @staticmethod
    async def get_or_create_user(session: AsyncSession, user_id: int, username: Optional[str] = None,
                                 first_name: Optional[str] = None, last_name: Optional[str] = None,
                                 language_code: Optional[str] = None) -> User:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.language_code = language_code
            await session.commit()
            logger.debug(f"Обновлен пользователь {user_id}")
        else:
            uid = await UserService.generate_unique_uid(session)
            user = User(id=user_id, uid=uid, username=username, first_name=first_name,
                       last_name=last_name, language_code=language_code)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logger.info(f"✅ Создан пользователь {user_id} с UID: {uid}")
        
        return user
    
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_uid(session: AsyncSession, uid: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.uid == uid))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def change_user_uid(session: AsyncSession, current_uid: int, new_uid: int) -> tuple[bool, str]:
        if new_uid < settings.MIN_UID or new_uid > settings.MAX_UID:
            return False, f"UID должен быть в диапазоне {settings.MIN_UID}-{settings.MAX_UID}"
        
        user = await UserService.get_user_by_uid(session, current_uid)
        if not user:
            return False, f"Пользователь с UID {current_uid} не найден"
        
        existing_user = await UserService.get_user_by_uid(session, new_uid)
        if existing_user:
            return False, f"UID {new_uid} уже занят пользователем @{existing_user.username}"
        
        old_uid = user.uid
        user.uid = new_uid
        await session.commit()
        
        logger.info(f"✅ UID изменен: {old_uid} -> {new_uid} для @{user.username}")
        return True, f"✅ UID успешно изменен с {old_uid} на {new_uid}"
    
    @staticmethod
    async def get_total_users(session: AsyncSession) -> int:
        result = await session.execute(select(func.count(User.id)))
        return result.scalar_one()
