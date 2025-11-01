"""
Обработчик команды /menu
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name='menu_command')


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Главное меню"""
    menu_text = (
        "📋 <b>Главное меню</b>\n\n"
        "Выберите раздел:\n\n"
        "📂 /catalog - Каталог услуг\n"
        "⭐ /gorateme - Подать в ТОП\n"
        "🔍 /search - Поиск\n"
        "🏆 /toppeople - Рейтинги\n"
        "❓ /help - Помощь\n"
    )
    
    await message.answer(menu_text)
