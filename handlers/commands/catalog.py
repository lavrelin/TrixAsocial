from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

router = Router(name='catalog_command')

@router.message(Command("catalog"))
async def cmd_catalog(message: Message):
    """Просмотр каталога (система 5 слотов)"""
    logger.info(f"Пользователь {message.from_user.id} запросил каталог")
    
    catalog_text = (
        "📂 <b>Каталог услуг</b>\n\n"
        "🔄 Система 5 слотов:\n"
        "• Slot 1-2: Обычные услуги\n"
        "• Slot 3: TopGirls/TopBoys\n"
        "• Slot 4: Приоритетные/Реклама\n"
        "• Slot 5: Специальный слот\n\n"
        "⚠️ <i>В разработке...</i>\n"
        "Здесь будут отображаться карточки услуг"
    )
    
    await message.answer(catalog_text)

@router.message(Command("search"))
async def cmd_search(message: Message):
    """Поиск по каталогу"""
    search_text = (
        "🔍 <b>Поиск по каталогу</b>\n\n"
        "Введите теги или название услуги для поиска\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(search_text)

@router.message(Command("review"))
async def cmd_review(message: Message):
    """Оставить отзыв"""
    review_text = (
        "💬 <b>Оставить отзыв</b>\n\n"
        "Формат: /review [номер карточки]\n"
        "Пример: /review 1234\n\n"
        "⏰ Кулдаун: 1 час на все отзывы\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(review_text)

@router.message(Command("categoryfollow"))
async def cmd_category_follow(message: Message):
    """Подписки на категории"""
    text = (
        "🔔 <b>Подписки на категории</b>\n\n"
        "Управление подписками на категории услуг\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)

@router.message(Command("myreviews"))
async def cmd_my_reviews(message: Message):
    """Мои отзывы"""
    text = (
        "📝 <b>Мои отзывы</b>\n\n"
        "Здесь будут ваши отзывы на карточки\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)
