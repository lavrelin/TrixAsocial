import random
from typing import List, Optional
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from DATABASE.catalog import CatalogPost, CatalogReview
from DATABASE.games import RatingPost

class CatalogService:
    """Сервис для работы с каталогом"""
    
    @staticmethod
    async def get_catalog_slots(session: AsyncSession, user_id: int, limit: int = 5) -> List[CatalogPost]:
        """
        Получить 5 слотов каталога:
        Slot 1-2: Обычные услуги
        Slot 3: TopGirls/TopBoys
        Slot 4: Приоритетные/Реклама
        Slot 5: Специальный слот
        """
        slots = []
        
        # Slot 1-2: Обычные услуги
        result = await session.execute(
            select(CatalogPost)
            .where(CatalogPost.is_active == True)
            .where(CatalogPost.is_priority == False)
            .where(CatalogPost.is_ad == False)
            .order_by(func.random())
            .limit(2)
        )
        slots.extend(result.scalars().all())
        
        # Slot 3: TopGirls или TopBoys (случайно)
        gender = random.choice(['girl', 'boy'])
        result = await session.execute(
            select(RatingPost)
            .where(RatingPost.status == 'approved')
            .where(RatingPost.gender == gender)
            .order_by(func.random())
            .limit(1)
        )
        rating_post = result.scalar_one_or_none()
        if rating_post:
            # Конвертируем в формат слота (опционально)
            pass
        
        # Slot 4: Приоритетные/Реклама
        result = await session.execute(
            select(CatalogPost)
            .where(CatalogPost.is_active == True)
            .where(or_(CatalogPost.is_priority == True, CatalogPost.is_ad == True))
            .order_by(func.random())
            .limit(1)
        )
        priority = result.scalar_one_or_none()
        if priority:
            slots.append(priority)
        
        # Slot 5: Обычный пост если нет специального
        if len(slots) < 5:
            result = await session.execute(
                select(CatalogPost)
                .where(CatalogPost.is_active == True)
                .order_by(func.random())
                .limit(5 - len(slots))
            )
            slots.extend(result.scalars().all())
        
        # Рандомизируем порядок слотов
        random.shuffle(slots)
        
        # Увеличиваем счетчик просмотров
        for post in slots:
            post.views += 1
        await session.commit()
        
        logger.debug(f"Сгенерировано {len(slots)} слотов для пользователя {user_id}")
        return slots[:limit]
    
    @staticmethod
    async def search_catalog(session: AsyncSession, query: str) -> List[CatalogPost]:
        """Поиск по каталогу"""
        search_pattern = f"%{query}%"
        
        result = await session.execute(
            select(CatalogPost)
            .where(CatalogPost.is_active == True)
            .where(
                or_(
                    CatalogPost.name.ilike(search_pattern),
                    CatalogPost.description.ilike(search_pattern),
                    CatalogPost.category.ilike(search_pattern)
                )
            )
            .order_by(CatalogPost.created_at.desc())
        )
        
        return result.scalars().all()
    
    @staticmethod
    async def get_post_by_number(session: AsyncSession, catalog_number: int) -> Optional[CatalogPost]:
        """Получить пост по номеру"""
        result = await session.execute(
            select(CatalogPost).where(CatalogPost.catalog_number == catalog_number)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_reviews(session: AsyncSession, user_id: int) -> List[CatalogReview]:
        """Получить отзывы пользователя"""
        result = await session.execute(
            select(CatalogReview)
            .where(CatalogReview.user_id == user_id)
            .order_by(CatalogReview.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def generate_catalog_number(session: AsyncSession) -> int:
        """Генерация уникального номера каталога (1-9999)"""
        from CORE.config import settings
        
        # Получаем занятые номера
        result = await session.execute(
            select(CatalogPost.catalog_number)
        )
        used_numbers = {row[0] for row in result.all()}
        
        # Также проверяем рейтинговые посты
        result = await session.execute(
            select(RatingPost.catalog_number)
        )
        used_numbers.update({row[0] for row in result.all()})
        
        # Находим свободный номер
        available = set(range(1, settings.MAX_CATALOG_NUMBER + 1)) - used_numbers
        
        if not available:
            raise ValueError("Нет доступных номеров каталога!")
        
        return random.choice(list(available))
