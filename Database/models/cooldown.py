"""
Модель кулдаунов команд
"""
from datetime import datetime

from sqlalchemy import BigInteger, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin


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
