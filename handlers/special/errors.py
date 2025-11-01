from aiogram import Router
from aiogram.types import ErrorEvent
from loguru import logger

router = Router(name='error_handler')

@router.errors()
async def error_handler(event: ErrorEvent):
    """Глобальный обработчик ошибок"""
    logger.exception(f"❌ Ошибка при обработке апдейта: {event.exception}")
    
    if event.update.message:
        try:
            await event.update.message.answer(
                "⚠️ Произошла ошибка при обработке команды.\n"
                "Попробуйте позже или обратитесь к администратору."
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {e}")
    
    # TODO: Отправить уведомление админам
    return True
