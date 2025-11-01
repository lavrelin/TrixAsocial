# database/__init__.py
from .base import engine, async_session_maker, Base

async def init_db():
    """Инициализация базы данных - создает только отсутствующие таблицы"""
    try:
        async with engine.begin() as conn:
            # Пробуем создать таблицы, игнорируем ошибки существования
            await conn.run_sync(Base.metadata.create_all)
        print("✅ База данных инициализирована")
        return True
    except Exception as e:
        if "already exists" in str(e):
            print("✅ Таблицы уже существуют")
            return True
        else:
            print(f"❌ Ошибка инициализации БД: {e}")
            return False

async def get_session():
    """Получение сессии для работы с БД"""
    async with async
