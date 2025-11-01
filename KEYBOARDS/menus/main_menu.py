from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню"""
    builder = ReplyKeyboardBuilder()
    
    builder.add(KeyboardButton(text="📂 Каталог"))
    builder.add(KeyboardButton(text="⭐ В ТОП"))
    builder.add(KeyboardButton(text="🔍 Поиск"))
    builder.add(KeyboardButton(text="🏆 Рейтинги"))
    builder.add(KeyboardButton(text="💬 Мои отзывы"))
    builder.add(KeyboardButton(text="❓ Помощь"))
    
    builder.adjust(2, 2, 2)
    
    return builder.as_markup(resize_keyboard=True)

def get_admin_menu() -> ReplyKeyboardMarkup:
    """Админ меню"""
    builder = ReplyKeyboardBuilder()
    
    builder.add(KeyboardButton(text="➕ Добавить в каталог"))
    builder.add(KeyboardButton(text="📊 Статистика"))
    builder.add(KeyboardButton(text="⚙️ Настройки"))
    builder.add(KeyboardButton(text="👥 Пользователи"))
    builder.add(KeyboardButton(text="📋 Модерация"))
    builder.add(KeyboardButton(text="🔙 Назад"))
    
    builder.adjust(2, 2, 2)
    
    return builder.as_markup(resize_keyboard=True)
