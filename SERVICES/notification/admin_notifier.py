from aiogram import Bot
from loguru import logger
from CORE.config import settings
from typing import Optional

class AdminNotifier:
    """Сервис для отправки уведомлений админам"""
    
    @staticmethod
    async def notify_new_rating_post(bot: Bot, post_id: int, username: str):
        """Уведомление о новой заявке в рейтинг"""
        message = (
            f"⭐ <b>Новая заявка в рейтинг</b>\n\n"
            f"От: @{username}\n"
            f"ID заявки: {post_id}\n\n"
            f"Требуется модерация!"
        )
        
        try:
            await bot.send_message(settings.ZAYAVKI_ID, message)
            logger.info(f"Отправлено уведомление о заявке {post_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления админам: {e}")
    
    @staticmethod
    async def notify_new_catalog_post(bot: Bot, catalog_number: int, category: str):
        """Уведомление о новой карточке каталога"""
        message = (
            f"📂 <b>Новая карточка в каталоге</b>\n\n"
            f"Номер: #{catalog_number}\n"
            f"Категория: {category}\n\n"
            f"Требуется модерация!"
        )
        
        try:
            await bot.send_message(settings.ZAYAVKI_ID, message)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")
    
    @staticmethod
    async def notify_error(bot: Bot, error_text: str, context: Optional[str] = None):
        """Уведомление об ошибке"""
        message = (
            f"❌ <b>Ошибка в боте</b>\n\n"
            f"{error_text}\n"
        )
        
        if context:
            message += f"\nКонтекст: {context}"
        
        try:
            await bot.send_message(settings.erranncom_ID, message)
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление об ошибке: {e}")
    
    @staticmethod
    async def send_stats_notification(bot: Bot, stats_text: str):
        """Отправка статистики"""
        try:
            await bot.send_message(settings.statification_ID, stats_text)
        except Exception as e:
            logger.error(f"Ошибка отправки статистики: {e}")
