"""
Обработчики админ команд
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from core.config import settings
from core.states import AdminStates
from services.admin_service import AdminService
from services.stats_service import StatsService
from database.base import get_session
from keyboards.inline import get_admin_menu

router = Router(name='admin_commands')


def is_admin(user_id: int) -> bool:
    """Проверка прав администратора"""
    return settings.is_admin(user_id)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Команда /admin - админ панель"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "⚙️ <b>Админ-панель</b>\n\n"
        "Доступные команды:\n"
        "/stats - Статистика бота\n"
        "/setslot - Установить специальный слот\n"
        "/moderation - Модерация контента\n"
        "/changeuid - Изменить UID пользователя\n"
        "/broadcast - Рассылка сообщений\n",
        reply_markup=get_admin_menu()
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Команда /stats - статистика бота"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    async for session in get_session():
        stats = await StatsService.get_full_statistics(session)
        
        text = (
            "📊 <b>Статистика бота</b>\n\n"
            f"👥 Всего пользователей: {stats['total_users']}\n"
            f"📂 Карточек в каталоге: {stats['catalog_posts']}\n"
            f"⭐ Рейтинговых постов: {stats['rating_posts']}\n"
            f"💬 Отзывов: {stats['reviews']}\n"
            f"🕐 Активных кулдаунов: {stats['active_cooldowns']}\n\n"
            f"📈 За сегодня:\n"
            f"• Новых пользователей: {stats['new_users_today']}\n"
            f"• Новых карточек: {stats['new_posts_today']}\n"
        )
        
        await message.answer(text)


@router.message(Command("setslot"))
async def cmd_setslot(message: Message, state: FSMContext):
    """Команда /setslot - установить специальный слот"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await state.set_state(AdminStates.waiting_for_slot_link)
    await message.answer(
        "🎰 <b>Установка специального слота</b>\n\n"
        "Отправьте ссылку на пост, который будет показываться в 5-м слоте.\n\n"
        "Пост будет показан 8-23 раза (случайное число).\n\n"
        "Для отмены напишите /cancel"
    )


@router.message(Command("moderation"))
async def cmd_moderation(message: Message):
    """Команда /moderation - модерация контента"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    async for session in get_session():
        pending = await AdminService.get_pending_moderation(session)
        
        if not pending:
            await message.answer("✅ Нет контента для модерации")
            return
        
        text = f"📋 <b>Ожидают модерации:</b> {len(pending)} элементов\n\n"
        
        for item in pending[:5]:
            text += f"• {item['type']}: {item['name']}\n"
        
        await message.answer(text)


@router.message(Command("changeuid"))
async def cmd_changeuid(message: Message):
    """Команда /changeuid - изменить UID пользователя"""
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
        success, result_message = await AdminService.change_user_uid(
            session=session,
            current_uid=current_uid,
            new_uid=new_uid
        )
        
        await message.answer(result_message)
        
        if success:
            logger.info(f"Admin {message.from_user.id} changed UID: {current_uid} -> {new_uid}")
