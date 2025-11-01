"""
Обработчики команд каталога
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from core.states import SearchStates, ReviewStates
from services.catalog_service import CatalogService
from keyboards.inline import get_catalog_navigation
from database.base import get_session

router = Router(name='catalog_commands')


@router.message(Command("catalog"))
async def cmd_catalog(message: Message):
    """Команда /catalog - просмотр каталога (5 слотов)"""
    logger.info(f"Пользователь {message.from_user.id} запросил каталог")
    
    async for session in get_session():
        slots = await CatalogService.get_catalog_slots(
            session=session,
            user_id=message.from_user.id
        )
        
        if not slots:
            await message.answer("📂 Каталог пока пуст")
            return
        
        text = "📂 <b>Каталог услуг Будапешта</b>\n\n"
        text += "🔄 Система 5 слотов:\n"
        text += "• Slot 1-2: Обычные услуги\n"
        text += "• Slot 3: TopGirls/TopBoys\n"
        text += "• Slot 4: Приоритетные/Реклама\n"
        text += "• Slot 5: Специальный слот\n\n"
        
        # Формируем текст из слотов
        for i, slot in enumerate(slots, 1):
            text += f"{i}. <b>{slot['name']}</b>\n"
            text += f"   Категория: {slot['category']}\n"
            text += f"   #{slot['catalog_number']}\n\n"
        
        await message.answer(
            text,
            reply_markup=get_catalog_navigation(page=0)
        )


@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    """Команда /search - поиск по каталогу"""
    await state.set_state(SearchStates.waiting_for_query)
    await message.answer(
        "🔍 <b>Поиск по каталогу</b>\n\n"
        "Введите теги или название услуги для поиска.\n"
        "Например: маникюр, массаж, фотограф\n\n"
        "Для отмены напишите /cancel"
    )


@router.message(Command("review"))
async def cmd_review(message: Message, state: FSMContext):
    """Команда /review - оставить отзыв"""
    await state.set_state(ReviewStates.waiting_for_catalog_number)
    await message.answer(
        "💬 <b>Оставить отзыв</b>\n\n"
        "Введите номер карточки каталога.\n"
        "Пример: 1234\n\n"
        "⏰ Внимание: можно оставлять 1 отзыв в час\n\n"
        "Для отмены напишите /cancel"
    )


@router.message(Command("myreviews"))
async def cmd_my_reviews(message: Message):
    """Команда /myreviews - мои отзывы"""
    async for session in get_session():
        reviews = await CatalogService.get_user_reviews(
            session=session,
            user_id=message.from_user.id
        )
        
        if not reviews:
            await message.answer("📝 У вас пока нет отзывов")
            return
        
        text = "📝 <b>Ваши отзывы</b>\n\n"
        for review in reviews[:10]:
            text += f"Карточка #{review.catalog_post_id}\n"
            text += f"Оценка: {'⭐' * review.rating}\n"
            text += f"Текст: {review.review_text[:100]}...\n\n"
        
        await message.answer(text)
