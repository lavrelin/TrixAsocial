"""
Конфигурация бота и переменные окружения
"""
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Настройки бота из переменных окружения"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Bot Configuration
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL Database URL")
    REDIS_URL: str = Field("redis://localhost:6379", description="Redis URL")
    
    # Channels
    MARKET_ID: int = Field(-1003033694255, description="Барахолка⚡️Будапешт")
    BPMAIN_ID: int = Field(-1002743668534, description="🛩️ БУДАПЕШТ")
    BPCHAT_ID: int = Field(-1002883770818, description="📨 Будапешт - чат")
    CATALOG_ID: int = Field(-1002601716810, description="КАТАЛОГ УСЛУГ 🛟")
    PARTNERS_ID: int = Field(-1002919380244, description="Budapest⛓️‍💥Partners")
    ASOCIAL_ID: int = Field(-1003088023508, description="A🫦Social")
    BATADAZE_ID: int = Field(-1003114019170, description="🃏batadaze")
    
    # Admin Chats
    ZAYAVKI_ID: int = Field(-1002734837434, description="xxx ♠️ users mssg/posts")
    ERRANNCOM_ID: int = Field(-1003039151203, description="xxx ♦️ commands, announce, errors")
    STATIFICATION_ID: int = Field(-4843909295, description="xxx ♣️ stats/notifications")
    
    # Admin IDs
    ADMIN_IDS: str = Field("", description="Comma-separated admin IDs")
    
    # Environment
    ENVIRONMENT: str = Field("production", description="Environment: development/production")
    DEBUG: bool = Field(False, description="Debug mode")
    
    # Reserved UIDs (cannot be auto-assigned)
    RESERVED_UIDS: List[int] = Field(
        default_factory=lambda: [
            1, 2, 3, 5, 7, 8, 10, 13, 17, 21, 22, 23, 25, 34, 42, 50, 53, 55, 69, 80, 89,
            112, 144, 187, 233, 255, 311, 360, 377, 420, 443, 451, 500, 511, 610, 666, 777,
            911, 987, 999, 1000, 1024, 1234, 1337, 1492, 1597, 1711, 1776, 1789, 1811, 1914,
            1917, 1941, 1945, 1961, 1969, 2584, 3276, 3306, 4096, 4181, 5000, 5318, 5432,
            6765, 6969, 8008, 9110, 9999, 10000, 10946, 11111, 17711, 21845, 28657, 32768,
            46368, 50000, 65535, 75025, 99999
        ]
    )
    
    # UID Range
    MIN_UID: int = Field(1, description="Minimum UID value")
    MAX_UID: int = Field(99999, description="Maximum UID value")
    
    # Cooldowns (in seconds)
    GORATEME_COOLDOWN: int = Field(10800, description="3 hours in seconds")
    REVIEW_COOLDOWN: int = Field(3600, description="1 hour in seconds")
    
    # Catalog Settings
    MAX_CATALOG_NUMBER: int = Field(9999, description="Maximum catalog number")
    CATALOG_SLOTS: int = Field(5, description="Number of catalog slots per page")
    MAX_PRIORITY_POSTS: int = Field(10, description="Maximum priority posts")
    
    # Rating Settings
    MIN_VOTE: int = Field(-2, description="Minimum vote value")
    MAX_VOTE: int = Field(2, description="Maximum vote value")
    MAX_ABOUT_WORDS: int = Field(3, description="Maximum words in 'about'")
    MAX_WORD_LENGTH: int = Field(7, description="Maximum length per word")
    
    def get_admin_ids(self) -> List[int]:
        """Получить список ID администраторов"""
        if not self.ADMIN_IDS:
            return []
        return [int(id.strip()) for id in self.ADMIN_IDS.split(",") if id.strip()]
    
    def is_admin(self, user_id: int) -> bool:
        """Проверить, является ли пользователь администратором"""
        return user_id in self.get_admin_ids()
    
    def is_reserved_uid(self, uid: int) -> bool:
        """Проверить, является ли UID зарезервированным"""
        return uid in self.RESERVED_UIDS


# Создаем глобальный экземпляр настроек
settings = Settings()


# Словарь категорий каталога
CATALOG_CATEGORIES = {
    "💇‍♀️ Красота и уход": [
        "Маникюр", "Стрижки", "Косметология", "Барбер", "Бьюти-процедуры",
        "Волосы", "Депиляция", "Эпиляция", "Ресницы и брови", "Тату", "Пирсинг"
    ],
    "🩺 Здоровье и тело": [
        "Ветеринар", "Врач", "Массажист", "Психолог", "Стоматолог",
        "Спорт", "Йога", "Фитнес", "Диетолог"
    ],
    "🛠️ Услуги и помощь": [
        "Автомеханик", "Грузчик", "Клининг", "Мастер по дому", "Перевозчик",
        "Ремонт техники", "Няня", "Юрист", "Бухгалтер", "IT-специалист", "Риелтор"
    ],
    "📚 Обучение и развитие": [
        "Курсы", "Онлайн-курсы", "Репетитор", "Переводчик", "Изучение английского",
        "Изучение венгерского", "Языковые школы", "Музыка"
    ],
    "🎭 Досуг и впечатления": [
        "Еда", "Фотограф", "Видеограф", "Экскурсии", "Для детей",
        "Аниматоры", "Организация праздников", "Швея", "Цветы", "Ремонт"
    ],
    "👱🏻‍♀️ TopGirls": ["TopGirls"],
    "🤵🏼‍♂️ TopBoys": ["TopBoys"]
}
