"""
FSM States для бота
"""
from aiogram.fsm.state import State, StatesGroup


class CatalogCreationStates(StatesGroup):
    """Состояния создания карточки каталога"""
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_tags = State()
    waiting_for_media = State()
    waiting_for_author_username = State()
    waiting_for_author_id = State()
    waiting_for_catalog_link = State()
    confirmation = State()


class RatingCreationStates(StatesGroup):
    """Состояния создания заявки в рейтинг /gorateme"""
    waiting_for_name = State()
    waiting_for_profile_url = State()
    waiting_for_about = State()
    waiting_for_gender = State()
    waiting_for_media = State()
    confirmation = State()


class ReviewStates(StatesGroup):
    """Состояния написания отзыва"""
    waiting_for_catalog_number = State()
    waiting_for_rating = State()
    waiting_for_review_text = State()
    confirmation = State()


class SearchStates(StatesGroup):
    """Состояния поиска по каталогу"""
    waiting_for_query = State()
    showing_results = State()


class AdminModerationStates(StatesGroup):
    """Состояния модерации контента"""
    viewing_item = State()
    editing_item = State()
    waiting_for_edit_field = State()
    waiting_for_new_value = State()


class AdminCatalogStates(StatesGroup):
    """Состояния админ-управления каталогом"""
    adding_priority = State()
    adding_reklama = State()
    setting_slot = State()
    waiting_for_post_link = State()


class AdminChangeUIDStates(StatesGroup):
    """Состояния изменения UID пользователя"""
    waiting_for_current_uid = State()
    waiting_for_new_uid = State()
    confirmation = State()
