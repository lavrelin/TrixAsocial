"""
Модели статистики и аналитики
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Date, String, Integer, BigInteger, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from DATABASE.base import Base, TimestampMixin


class Statistics(Base, TimestampMixin):
    """Модель статистики"""
    __tablename__ = "statistics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    stat_date: Mapped[datetime] = mapped_column(Date, index=True)
    stat_type: Mapped[str] = mapped_column(String(50), index=True)  # 'users', 'catalog', 'ratings', 'commands'
    
    # Значение может быть числом или JSON
    value: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    value_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Statistics {self.stat_type} {self.stat_date}>"
