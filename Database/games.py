"""
Модели игр и рейтингов
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, Integer, Boolean, Text, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from DATABASE.base import Base, TimestampMixin


class RatingPost(Base, TimestampMixin):
    """Модель рейтингового поста TopPeople"""
    __tablename__ = "rating_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Уникальный номер (1-9999, общий пул с каталогом)
    catalog_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    
    # Основная информация
    name: Mapped[str] = mapped_column(String(255))
    profile_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Instagram/Telegram
    about: Mapped[str] = mapped_column(String(255))  # 3 слова × 7 символов
    gender: Mapped[str] = mapped_column(String(10), index=True)  # 'boy'/'girl'
    
    # Медиа
    media_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    media_file_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Автор заявки
    author_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    author_username: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Модерация
    status: Mapped[str] = mapped_column(String(50), default='pending', index=True)  # pending/approved/rejected
    published_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    moderation_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    # Голосование
    votes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)  # {"user_id": vote_value}
    total_score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self):
        return f"<RatingPost #{self.catalog_number} {self.name} score:{self.total_score}>"


class RatingVote(Base, TimestampMixin):
    """Модель голосов в рейтинге"""
    __tablename__ = "rating_votes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    rating_post_id: Mapped[int] = mapped_column(Integer, ForeignKey("rating_posts.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    
    vote_value: Mapped[int] = mapped_column(Integer)  # -2 to +2
    
    __table_args__ = (
        UniqueConstraint('rating_post_id', 'user_id', name='unique_user_vote'),
    )
    
    def __repr__(self):
        return f"<RatingVote post:{self.rating_post_id} user:{self.user_id} vote:{self.vote_value}>"


class Cooldown(Base, TimestampMixin):
    """Модель кулдаунов команд"""
    __tablename__ = "cooldowns"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    command: Mapped[str] = mapped_column(String(50), index=True)  # 'gorateme', 'review'
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'command', name='unique_user_cooldown'),
    )
    
    def __repr__(self):
        return f"<Cooldown user:{self.user_id} cmd:{self.command}>"
