"""
Core модуль - ядро бота
"""
from .config import settings
from .bot import bot
from .dispatcher import setup_dispatcher

__all__ = ['settings', 'bot', 'setup_dispatcher']
