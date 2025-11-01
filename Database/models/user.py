"""
Модель пользователя
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """Модель пользователя"""
    __tablename__ = "users"
    
    # Telegram ID как primary key
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    # Уникальный UID (1-99999, исключая зарезервированные)
    uid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    
    # Информация о пользователе
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # Статусы
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Активность
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self):
        return f"<User {self.id} (@{self.username}) UID:{self.uid}>"
