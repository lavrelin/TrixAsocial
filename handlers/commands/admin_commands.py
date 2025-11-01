"""
Админ команды
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from DATABASE.base import get_session
from SERVICES.database.user_service import UserService
from CORE.config import settings
from CORE.states import AdminChangeUIDStates

router = Router(name='admin_commands')


def is_admin(user_id: int) -> bool:
    """Проверка прав администратора"""
    return settings.is_admin(user_id)


@router.message(Command("changeuid"))
async def cmd_change_uid(message: Message, state: FSMContext):
    """Команда изменения UID: /changeuid <current_uid> <new_uid>"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    # Проверяем аргументы
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
            session=session,
            current_uid=current_uid,
            new_uid=new_uid
        )
        
        await message.answer(result_message)
        
        if success:
            logger.info(f"Admin {message.from_user.id} changed UID: {current_uid} -> {new_uid}")


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика бота"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    async for session in get_session():
        total_users = await UserService.get_total_users(session)
        
        stats_text = (
            "📊 <b>Статистика бота</b>\n\n"
            f"👥 Всего пользователей: {total_users}\n"
            f"📋 Активных карточек: 0\n"  # TODO: добавить подсчет
            f"⭐ Рейтинговых постов: 0\n"  # TODO: добавить подсчет
            f"💬 Отзывов: 0\n"  # TODO: добавить подсчет
        )
        
        await message.answer(stats_text)


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """Рассылка сообщений всем пользователям"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "📢 Функция рассылки\n\n"
        "⚠️ В разработке"
    )


@router.message(Command("addtocatalog"))
async def cmd_add_to_catalog(message: Message):
    """Добавить услугу в каталог"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "📂 Добавление услуги в каталог\n\n"
        "⚠️ В разработке"
    )


@router.message(Command("catalogpriority"))
async def cmd_catalog_priority(message: Message):
    """Управление приоритетными постами"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "⭐ Управление приоритетными постами\n\n"
        "⚠️ В разработке"
    )


@router.message(Command("setslot"))
async def cmd_set_slot(message: Message):
    """Настройка специального слота"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "🎰 Настройка специального слота\n\n"
        "⚠️ В разработке"
    )


@router.message(Command("toppeoplereset"))
async def cmd_top_people_reset(message: Message):
    """Сброс рейтинга TopPeople"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    await message.answer(
        "🔄 Сброс рейтинга TopPeople\n\n"
        "⚠️ Эта команда удалит все голоса и рейтинги!\n"
        "Для подтверждения напишите: /confirm_reset"
    )
