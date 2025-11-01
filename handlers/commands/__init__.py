"""
Обработчики команд
"""
from . import start_handler
from . import help_handler
from . import catalog_handler
from . import rating_handler
from . import admin_handler

__all__ = [
    'start_handler',
    'help_handler',
    'catalog_handler',
    'rating_handler',
    'admin_handler'
]
