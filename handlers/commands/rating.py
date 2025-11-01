from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

router = Router(name='rating_command')

@router.message(Command("gorateme"))
async def cmd_go_rate_me(message: Message):
    """Подать заявку в рейтинг TopPeople"""
    logger.info(f"Пользователь {message.from_user.id} хочет подать заявку в рейтинг")
    
    text = (
        "⭐ <b>Заявка в ТОП</b>\n\n"
        "Заполните анкету:\n"
        "1️⃣ Имя\n"
        "2️⃣ Профиль (Instagram/Telegram)\n"
        "3️⃣ О себе (3 слова × 7 символов)\n"
        "4️⃣ Пол (для категории TopGirls/TopBoys)\n"
        "5️⃣ Фото/Видео\n\n"
        "⏰ Кулдаун: 3 часа\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)

@router.message(Command("toppeople"))
async def cmd_top_people(message: Message):
    """Топ-10 всех пользователей"""
    text = (
        "🏆 <b>ТОП-10 Пользователей</b>\n\n"
        "Рейтинг формируется на основе голосования\n"
        "Голоса: от -2 до +2\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)

@router.message(Command("topboys"))
async def cmd_top_boys(message: Message):
    """Топ-10 парней"""
    text = (
        "🤵🏼‍♂️ <b>ТОП-10 Парней</b>\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)

@router.message(Command("topgirls"))
async def cmd_top_girls(message: Message):
    """Топ-10 девушек"""
    text = (
        "👱🏻‍♀️ <b>ТОП-10 Девушек</b>\n\n"
        "⚠️ <i>В разработке...</i>"
    )
    
    await message.answer(text)
