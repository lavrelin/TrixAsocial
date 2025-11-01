from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name='help_command')

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "❓ <b>Помощь по командам TrixBot</b>\n\n"
        "<b>📂 Каталог услуг:</b>\n"
        "/catalog - Просмотр каталога (5 слотов)\n"
        "/search - Поиск по тегам и названиям\n"
        "/review [номер] - Оставить отзыв на карточку\n"
        "/categoryfollow - Подписаться на категории\n"
        "/myreviews - Мои отзывы\n\n"
        "<b>⭐ Рейтинги:</b>\n"
        "/gorateme - Подать заявку в ТОП (кулдаун 3 часа)\n"
        "/toppeople - Топ-10 всех\n"
        "/topboys - Топ-10 парней\n"
        "/topgirls - Топ-10 девушек\n\n"
        "<b>ℹ️ Информация:</b>\n"
        "/start - Начать работу\n"
        "/help - Эта справка\n\n"
        "💡 <i>Совет: используйте кнопки-подсказки в сообщениях бота</i>"
    )
    await message.answer(help_text)
