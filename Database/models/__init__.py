"""
Модели базы данных
"""
from .user import User
from .catalog import CatalogPost, CatalogReview
from .rating import RatingPost, RatingVote
from .cooldown import Cooldown
from .special_slot import SpecialSlot

__all__ = [
    'User', 'CatalogPost', 'CatalogReview',
    'RatingPost', 'RatingVote', 'Cooldown',
    'SpecialSlot'
]
