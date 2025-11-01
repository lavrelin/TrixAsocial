from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_gender_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора пола для рейтинга"""
    keyboard = [
        [
            InlineKeyboardButton(text="👱🏻‍♀️ Девушка", callback_data="gender:girl"),
            InlineKeyboardButton(text="🤵🏼‍♂️ Парень", callback_data="gender:boy")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_vote_keyboard(rating_post_id: int) -> InlineKeyboardMarkup:
    """Клавиатура голосования (-2 до +2)"""
    keyboard = [
        [
            InlineKeyboardButton(text="--", callback_data=f"vote:{rating_post_id}:-2"),
            InlineKeyboardButton(text="-", callback_data=f"vote:{rating_post_id}:-1"),
            InlineKeyboardButton(text="0", callback_data=f"vote:{rating_post_id}:0"),
            InlineKeyboardButton(text="+", callback_data=f"vote:{rating_post_id}:1"),
            InlineKeyboardButton(text="++", callback_data=f"vote:{rating_post_id}:2"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_moderation_keyboard(rating_post_id: int) -> InlineKeyboardMarkup:
    """Клавиатура модерации заявки"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"mod_approve:{rating_post_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"mod_reject:{rating_post_id}")
        ],
        [
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"mod_edit:{rating_post_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
