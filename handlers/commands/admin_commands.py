from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from DATABASE.base import get_session
from SERVICES.database.user_service import UserService
from CORE.config import settings

router = Router(name='admin_commands')

def is_admin(user_id: int) -> bool:
    return settings.is_admin(user_id)

@router.message(Command("changeuid"))
async def cmd_change_uid(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer(
            "❌ Неверный формат команды\n\n"
            "Используйте: /changeuid <current_uid> <new_uid>\n"
            "Пример: /changeuid 12345 99999"
        )
        return
    
    try:
        current_uid = int(args[1])
        new_uid = int(args[2])
    except ValueError:
        await message.answer("❌ UID должны быть числами")
        return
    
    async for session in get_session():
        success, result_message = await UserService.change_user_uid(
            session=session, current_uid=current_uid, new_uid=new_uid
        )
        
        await message.answer(result_message)
        
        if success:
            logger.info(f"Admin {message.from_user.id} changed UID: {current_uid} -> {new_uid}")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    async for session in get_session():
        from SERVICES.database.catalog_service import CatalogService
        from SERVICES.database.rating_service import RatingService
        
        total_users = await UserService.get_total_users(session)
        total_catalog = await CatalogService.get_total_posts(session)
        total_ratings = await RatingService.get_total_rating_posts(session)
        
        stats_text = (
            "📊 <b>Статистика бота</b>\n\n"
            f"👥 Всего пользователей: {total_users}\n"
            f"📋 Активных карточек: {total_catalog}\n"
            f"⭐ Рейтинговых постов: {total_ratings}\n"
            f"💬 Отзывов: 0\n"
        )
        
        await message.answer(stats_text)
