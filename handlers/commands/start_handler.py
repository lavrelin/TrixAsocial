"""
Обработчик команды /start
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from database.base import get_session
from services.user_service import UserService
from keyboards.reply import get_main_menu

router = Router(name='start_command')


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Команда /start - регистрация пользователя с UID"""
    user = message.from_user
    
    async for session in get_session():
        db_user = await UserService.get_or_create_user(
            session=session,
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code
        )
        
        logger.info(f"👤 Пользователь {user.id} запустил бота")
        
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            f"Добро пожаловать в <b>TrixBot♥️</b> - Будапешт!\n\n"
            f"🆔 Ваш уникальный ID: <b>{db_user.uid}</b>\n\n"
            f"📋 Основные команды:\n"
            f"/catalog - 📂 Каталог услуг\n"
            f"/gorateme - ⭐ Подать заявку в ТОП\n"
            f"/search - 🔍 Поиск по каталогу\n"
            f"/review - 💬 Оставить отзыв\n"
            f"/toppeople - 🏆 Топ пользователей\n"
            f"/help - ❓ Помощь\n"
        )
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu(is_admin=db_user.is_admin)
        )
