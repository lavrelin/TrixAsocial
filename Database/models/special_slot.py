"""
Модель специального слота /setslot
"""
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin


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
