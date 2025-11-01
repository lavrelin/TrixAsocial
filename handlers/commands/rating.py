"""
Обработчики команд рейтинга
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from core.states import RatingStates
from services.rating_service import RatingService
from services.cooldown_service import CooldownService
from database.base import get_session
from keyboards.inline import get_gender_keyboard

router = Router(name='rating_commands')


@router.message(Command("gorateme"))
async def cmd_gorateme(message: Message, state: FSMContext):
    """Команда /gorateme - подать заявку в рейтинг"""
    logger.info(f"Пользователь {message.from_user.id} хочет подать заявку в рейтинг")
    
    async for session in get_session():
        # Проверяем кулдаун
        can_use, time_left = await CooldownService.check_cooldown(
            session=session,
            user_id=message.from_user.id,
            command='gorateme'
        )
        
        if not can_use:
            hours = time_left // 3600
            minutes = (time_left % 3600) // 60
            await message.answer(
                f"⏰ Вы недавно подавали заявку в ТОП\n\n"
                f"Попробуйте через {hours}ч {minutes}мин"
            )
            return
        
        await state.set_state(RatingStates.waiting_for_name)
        await message.answer(
            "⭐ <b>Подать заявку в ТОП</b>\n\n"
            "Шаг 1/5: Введите ваше имя\n\n"
            "Это имя будет показано в рейтинге.\n"
            "Для отмены напишите /cancel"
        )


@router.message(Command("toppeople"))
async def cmd_toppeople(message: Message):
    """Команда /toppeople - топ всех"""
    async for session in get_session():
        posts = await RatingService.get_top_ratings(
            session=session,
            limit=10
        )
        
        if not posts:
            await message.answer("🏆 Рейтинг пока пуст")
            return
        
        text = "🏆 <b>ТОП-10 людей Будапешта</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} <b>{post.name}</b>\n"
            text += f"    О себе: {post.about}\n"
            text += f"    Рейтинг: {post.total_score} ({post.vote_count} голосов)\n\n"
        
        await message.answer(text)


@router.message(Command("topboys"))
async def cmd_topboys(message: Message):
    """Команда /topboys - топ парней"""
    async for session in get_session():
        posts = await RatingService.get_top_ratings(
            session=session,
            gender='boy',
            limit=10
        )
        
        if not posts:
            await message.answer("🤵🏼‍♂️ Рейтинг TopBoys пока пуст")
            return
        
        text = "🤵🏼‍♂️ <b>ТОП-10 парней</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} <b>{post.name}</b> - {post.total_score} баллов\n"
        
        await message.answer(text)


@router.message(Command("topgirls"))
async def cmd_topgirls(message: Message):
    """Команда /topgirls - топ девушек"""
    async for session in get_session():
        posts = await RatingService.get_top_ratings(
            session=session,
            gender='girl',
            limit=10
        )
        
        if not posts:
            await message.answer("👱🏻‍♀️ Рейтинг TopGirls пока пуст")
            return
        
        text = "👱🏻‍♀️ <b>ТОП-10 девушек</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} <b>{post.name}</b> - {post.total_score} баллов\n"
        
        await message.answer(text)
