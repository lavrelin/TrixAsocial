"""
Модели постов и модерации
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from DATABASE.base import Base, TimestampMixin


class ModerationQueue(Base, TimestampMixin):
    """Модель очереди модерации"""
    __tablename__ = "moderation_queue"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    content_type: Mapped[str] = mapped_column(String(50), index=True)  # 'catalog', 'rating', 'review'
    content_id: Mapped[int] = mapped_column(Integer, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default='pending', index=True)  # pending/approved/rejected
    moderator_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    moderated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<ModerationQueue {self.content_type}:{self.content_id} status:{self.status}>"


class SpecialSlot(Base, TimestampMixin):
    """Модель специального слота /setslot"""
    __tablename__ = "special_slots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    post_link: Mapped[str] = mapped_column(String(500))
    
    # Счетчики показов
    total_shows: Mapped[int] = mapped_column(Integer, default=0)
    target_shows: Mapped[int] = mapped_column(Integer)  # 8-23 случайное число
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    
    def __repr__(self):
        return f"<SpecialSlot {self.total_shows}/{self.target_shows}>"
