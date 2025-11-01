from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from DATABASE.games import RatingPost, RatingVote
from SERVICES.database.catalog_service import CatalogService

class RatingService:
    """Сервис для работы с рейтингами"""
    
    @staticmethod
    async def create_rating_post(
        session: AsyncSession,
        user_id: int,
        username: Optional[str],
        name: str,
        profile_url: Optional[str],
        about: str,
        gender: str,
        media_type: str,
        media_file_id: str
    ) -> Tuple[bool, str]:
        """Создать заявку в рейтинг"""
        try:
            # Генерируем уникальный номер каталога
            catalog_number = await CatalogService.generate_catalog_number(session)
            
            rating_post = RatingPost(
                catalog_number=catalog_number,
                name=name,
                profile_url=profile_url,
                about=about,
                gender=gender,
                media_type=media_type,
                media_file_id=media_file_id,
                author_user_id=user_id,
                author_username=username,
                status='pending'
            )
            
            session.add(rating_post)
            await session.commit()
            await session.refresh(rating_post)
            
            logger.info(f"Создана заявка в рейтинг #{catalog_number} от пользователя {user_id}")
            return True, f"Заявка #{catalog_number} создана"
            
        except Exception as e:
            logger.error(f"Ошибка создания заявки в рейтинг: {e}")
            return False, str(e)
    
    @staticmethod
    async def get_top_ratings(
        session: AsyncSession,
        gender: Optional[str] = None,
        limit: int = 10
    ) -> List[RatingPost]:
        """Получить топ рейтингов"""
        query = select(RatingPost).where(RatingPost.status == 'approved')
        
        if gender:
            query = query.where(RatingPost.gender == gender)
        
        query = query.order_by(RatingPost.total_score.desc()).limit(limit)
        
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def vote_for_post(
        session: AsyncSession,
        rating_post_id: int,
        user_id: int,
        vote_value: int
    ) -> Tuple[bool, str]:
        """Проголосовать за пост в рейтинге"""
        from CORE.config import settings
        
        # Валидация голоса
        if vote_value < settings.MIN_VOTE or vote_value > settings.MAX_VOTE:
            return False, f"Голос должен быть от {settings.MIN_VOTE} до {settings.MAX_VOTE}"
        
        # Проверяем существование поста
        result = await session.execute(
            select(RatingPost).where(RatingPost.id == rating_post_id)
        )
        post = result.scalar_one_or_none()
        if not post:
            return False, "Пост не найден"
        
        # Проверяем, не голосовал ли уже
        result = await session.execute(
            select(RatingVote).where(
                RatingVote.rating_post_id == rating_post_id,
                RatingVote.user_id == user_id
            )
        )
        existing_vote = result.scalar_one_or_none()
        
        if existing_vote:
            return False, "Вы уже голосовали за этот пост"
        
        # Создаем голос
        vote = RatingVote(
            rating_post_id=rating_post_id,
            user_id=user_id,
            vote_value=vote_value
        )
        session.add(vote)
        
        # Обновляем рейтинг поста
        post.total_score += vote_value
        post.vote_count += 1
        
        await session.commit()
        
        logger.info(f"Пользователь {user_id} проголосовал {vote_value} за пост {rating_post_id}")
        return True, "Голос учтен!"
    
    @staticmethod
    async def approve_rating_post(
        session: AsyncSession,
        rating_post_id: int,
        published_link: str
    ) -> Tuple[bool, str]:
        """Одобрить заявку в рейтинг (админ)"""
        result = await session.execute(
            select(RatingPost).where(RatingPost.id == rating_post_id)
        )
        post = result.scalar_one_or_none()
        
        if not post:
            return False, "Пост не найден"
        
        post.status = 'approved'
        post.published_link = published_link
        await session.commit()
        
        logger.info(f"Заявка {rating_post_id} одобрена")
        return True, "Заявка одобрена"
