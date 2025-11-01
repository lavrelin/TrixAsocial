from datetime import datetime, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from DATABASE.users import User
from DATABASE.catalog import CatalogPost
from DATABASE.games import RatingPost
from DATABASE.analytics import Statistics

class StatsCollector:
    """Сборщик статистики"""
    
    @staticmethod
    async def collect_daily_stats(session: AsyncSession) -> dict:
        """Собрать дневную статистику"""
        today = date.today()
        
        # Общее количество пользователей
        result = await session.execute(select(func.count(User.id)))
        total_users = result.scalar_one()
        
        # Новые пользователи за сегодня
        result = await session.execute(
            select(func.count(User.id))
            .where(func.date(User.created_at) == today)
        )
        new_users_today = result.scalar_one()
        
        # Активных карточек
        result = await session.execute(
            select(func.count(CatalogPost.id))
            .where(CatalogPost.is_active == True)
        )
        active_cards = result.scalar_one()
        
        # Рейтинговых постов
        result = await session.execute(
            select(func.count(RatingPost.id))
            .where(RatingPost.status == 'approved')
        )
        rating_posts = result.scalar_one()
        
        stats = {
            'date': today,
            'total_users': total_users,
            'new_users_today': new_users_today,
            'active_cards': active_cards,
            'rating_posts': rating_posts
        }
        
        # Сохраняем в БД
        stat_record = Statistics(
            stat_date=today,
            stat_type='daily_summary',
            value_json=stats
        )
        session.add(stat_record)
        await session.commit()
        
        logger.info(f"Собрана статистика за {today}")
        return stats
    
    @staticmethod
    async def get_stats_text(session: AsyncSession) -> str:
        """Получить текст статистики"""
        stats = await StatsCollector.collect_daily_stats(session)
        
        text = (
            f"📊 <b>Статистика на {stats['date']}</b>\n\n"
            f"👥 Всего пользователей: {stats['total_users']}\n"
            f"🆕 Новых за сегодня: {stats['new_users_today']}\n"
            f"📋 Активных карточек: {stats['active_cards']}\n"
            f"⭐ Рейтинговых постов: {stats['rating_posts']}\n"
        )
        
        return text
