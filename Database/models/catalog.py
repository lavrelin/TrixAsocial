"""
Модели каталога услуг
"""
from typing import Optional

from sqlalchemy import BigInteger, String, Integer, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin


class CatalogPost(Base, TimestampMixin):
    """Модель карточки каталога"""
    __tablename__ = "catalog_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Уникальный номер карточки (1-9999)
    catalog_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    
    # Создатель карточки
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    
    # Категория и информация
    category: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Теги (JSON массив)
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Ссылка на оригинальный пост в канале
    catalog_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Медиа контент
    media_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'photo', 'video'
    media_file_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    media_group_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Автор услуги (может отличаться от создателя)
    author_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    author_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    # Статистика
    views: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    
    # Флаги
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_priority: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_ad: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    reviews = relationship("CatalogReview", back_populates="catalog_post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CatalogPost #{self.catalog_number} {self.name}>"


class CatalogReview(Base, TimestampMixin):
    """Модель отзыва на карточку каталога"""
    __tablename__ = "catalog_reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Карточка каталога
    catalog_post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("catalog_posts.id", ondelete="CASCADE"), index=True
    )
    
    # Автор отзыва
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Содержание отзыва
    review_text: Mapped[str] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer)  # 1-5 звезд
    
    # Модерация
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
    # Relationships
    catalog_post = relationship("CatalogPost", back_populates="reviews")
    
    def __repr__(self):
        return f"<CatalogReview #{self.id} rating:{self.rating}/5>"
