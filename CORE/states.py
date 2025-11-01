"""
FSM States для бота
"""
from aiogram.fsm.state import State, StatesGroup


class CatalogStates(StatesGroup):
    """Состояния создания карточки каталога"""
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_tags = State()
    waiting_for_media = State()
    waiting_for_author = State()
    confirmation = State()


class RatingStates(StatesGroup):
    """Состояния создания заявки в рейтинг /gorateme"""
    waiting_for_name = State()
    waiting_for_profile = State()
    waiting_for_about = State()
    waiting_for_gender = State()
    waiting_for_media = State()
    confirmation = State()


class ReviewStates(StatesGroup):
    """Состояния написания отзыва"""
    waiting_for_catalog_number = State()
    waiting_for_rating = State()
    waiting_for_text = State()
    confirmation = State()


class SearchStates(StatesGroup):
    """Состояния поиска по каталогу"""
    waiting_for_query = State()
    showing_results = State()


class AdminStates(StatesGroup):
    """Состояния админ-панели"""
    moderation_menu = State()
    editing_post = State()
    setting_slot = State()
    waiting_for_slot_link = State()
