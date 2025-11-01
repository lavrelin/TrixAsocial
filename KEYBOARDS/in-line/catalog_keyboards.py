from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_catalog_navigation(current_page: int = 0, total_pages: int = 1) -> InlineKeyboardMarkup:
    """Клавиатура навигации по каталогу"""
    keyboard = []
    
    # Кнопки навигации
    nav_row = []
    if current_page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"catalog_page:{current_page-1}"))
    
    nav_row.append(InlineKeyboardButton(text=f"{current_page+1}/{total_pages}", callback_data="catalog_current"))
    
    if current_page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"catalog_page:{current_page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Дополнительные действия
    keyboard.append([
        InlineKeyboardButton(text="🔍 Поиск", callback_data="catalog_search"),
        InlineKeyboardButton(text="📂 Категории", callback_data="catalog_categories")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_post_actions(catalog_number: int) -> InlineKeyboardMarkup:
    """Клавиатура действий с карточкой"""
    keyboard = [
        [
            InlineKeyboardButton(text="💬 Оставить отзыв", callback_data=f"review:{catalog_number}"),
            InlineKeyboardButton(text="📊 Статистика", callback_data=f"stats:{catalog_number}")
        ],
        [
            InlineKeyboardButton(text="🔗 Открыть пост", url=f"https://t.me/catalogtrix/{catalog_number}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура категорий каталога"""
    from CORE.config import CATALOG_CATEGORIES
    
    keyboard = []
    
    for category_name in CATALOG_CATEGORIES.keys():
        keyboard.append([
            InlineKeyboardButton(
                text=category_name,
                callback_data=f"category:{category_name}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="catalog_back")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
