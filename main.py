"""
TrixBot - Telegram Bot для Будапешта
Единый файл со всем функционалом
"""
import os
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional, List

# Aiogram imports
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# SQLAlchemy imports
from sqlalchemy import BigInteger, String, Boolean, Integer, Text, JSON, DateTime, ForeignKey, UniqueConstraint, select, func, or_, delete, Date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# ====================== CONFIG ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

RESERVED_UIDS = [
    1, 2, 3, 5, 7, 8, 10, 13, 17, 21, 22, 23, 25, 34, 42, 50, 53, 55, 69, 80, 89,
    112, 144, 187, 233, 255, 311, 360, 377, 420, 443, 451, 500, 511, 610, 666, 777,
    911, 987, 999, 1000, 1024, 1234, 1337, 1492, 1597, 1711, 1776, 1789, 1811, 1914,
    1917, 1941, 1945, 1961, 1969, 2584, 3276, 3306, 4096, 4181, 5000, 5318, 5432,
    6765, 6969, 8008, 9110, 9999, 10000, 10946, 11111, 17711, 21845, 28657, 32768,
    46368, 50000, 65535, 75025, 99999
]

# ====================== DATABASE MODELS ======================
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    message_count: Mapped[int] = mapped_column(Integer, default=0)

class CatalogPost(Base):
    __tablename__ = "catalog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    catalog_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class RatingPost(Base):
    __tablename__ = "rating_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    catalog_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    profile_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    about: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(String(10))
    media_type: Mapped[str] = mapped_column(String(50))
    media_file_id: Mapped[str] = mapped_column(String(500))
    author_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    author_username: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default='pending')
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class RatingVote(Base):
    __tablename__ = "rating_votes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating_post_id: Mapped[int] = mapped_column(Integer, ForeignKey("rating_posts.id"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    vote_value: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('rating_post_id', 'user_id', name='unique_user_vote'),)

class Cooldown(Base):
    __tablename__ = "cooldowns"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    command: Mapped[str] = mapped_column(String(50))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('user_id', 'command', name='unique_user_cooldown'),)

# ====================== DATABASE SETUP ======================
engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized")

async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

# ====================== FSM STATES ======================
class RatingStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_profile = State()
    waiting_for_about = State()
    waiting_for_gender = State()
    waiting_for_media = State()

# ====================== SERVICES ======================
async def generate_uid(session: AsyncSession) -> int:
    """Generate unique UID excluding reserved numbers"""
    result = await session.execute(select(User.uid))
    used_uids = {row[0] for row in result.all()}
    available = set(range(1, 100000)) - set(RESERVED_UIDS) - used_uids
    if not available:
        raise ValueError("No available UIDs")
    return random.choice(list(available))

async def get_or_create_user(session: AsyncSession, user_id: int, username: str = None, 
                             first_name: str = None, last_name: str = None) -> User:
    """Get or create user with UID"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        uid = await generate_uid(session)
        user = User(id=user_id, uid=uid, username=username, first_name=first_name, last_name=last_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"✅ Created user {user_id} with UID {uid}")
    else:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.last_activity = datetime.utcnow()
        user.message_count += 1
        await session.commit()
    
    return user

async def check_cooldown(session: AsyncSession, user_id: int, command: str) -> tuple[bool, int]:
    """Check if user can use command"""
    # Delete expired cooldowns
    await session.execute(delete(Cooldown).where(Cooldown.expires_at < datetime.utcnow()))
    await session.commit()
    
    result = await session.execute(
        select(Cooldown).where(Cooldown.user_id == user_id, Cooldown.command == command)
    )
    cooldown = result.scalar_one_or_none()
    
    if not cooldown:
        return True, 0
    
    time_left = int((cooldown.expires_at - datetime.utcnow()).total_seconds())
    return time_left <= 0, max(0, time_left)

async def set_cooldown(session: AsyncSession, user_id: int, command: str, seconds: int):
    """Set cooldown for command"""
    await session.execute(delete(Cooldown).where(Cooldown.user_id == user_id, Cooldown.command == command))
    cooldown = Cooldown(user_id=user_id, command=command, expires_at=datetime.utcnow() + timedelta(seconds=seconds))
    session.add(cooldown)
    await session.commit()

async def generate_catalog_number(session: AsyncSession) -> int:
    """Generate unique catalog number (1-9999)"""
    result = await session.execute(select(CatalogPost.catalog_number))
    used = {r[0] for r in result.all()}
    result = await session.execute(select(RatingPost.catalog_number))
    used.update({r[0] for r in result.all()})
    available = set(range(1, 10000)) - used
    if not available:
        raise ValueError("No available catalog numbers")
    return random.choice(list(available))

# ====================== BOT & DISPATCHER ======================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# ====================== HANDLERS ======================

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start command - register user with UID"""
    async for session in get_session():
        user = await get_or_create_user(
            session, message.from_user.id, message.from_user.username,
            message.from_user.first_name, message.from_user.last_name
        )
        
        await message.answer(
            f"👋 Привет, {user.first_name}!\n\n"
            f"Добро пожаловать в TrixBot♥️ - Будапешт!\n\n"
            f"🆔 Ваш уникальный ID: <b>{user.uid}</b>\n\n"
            f"📋 Команды:\n"
            f"/catalog - 📂 Каталог услуг\n"
            f"/gorateme - ⭐ Подать в ТОП\n"
            f"/toppeople - 🏆 Рейтинг\n"
            f"/help - ❓ Помощь\n"
        )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Help command"""
    await message.answer(
        "❓ <b>Помощь по командам TrixBot</b>\n\n"
        "<b>Основные:</b>\n"
        "/start - Начать работу\n"
        "/help - Эта справка\n\n"
        "<b>Каталог:</b>\n"
        "/catalog - Просмотр каталога\n\n"
        "<b>Рейтинги:</b>\n"
        "/gorateme - Подать заявку в ТОП (кулдаун 3 часа)\n"
        "/toppeople - Топ-10 всех\n"
        "/topboys - Топ-10 парней\n"
        "/topgirls - Топ-10 девушек\n\n"
        "<b>Админ:</b>\n"
        "/stats - Статистика\n"
        "/changeuid - Изменить UID\n"
    )

@router.message(Command("catalog"))
async def cmd_catalog(message: Message):
    """Show catalog - random 5 posts"""
    async for session in get_session():
        result = await session.execute(
            select(CatalogPost).where(CatalogPost.is_active == True)
            .order_by(func.random()).limit(5)
        )
        posts = result.scalars().all()
        
        if not posts:
            await message.answer("📂 Каталог пока пуст")
            return
        
        text = "📂 <b>Каталог услуг Будапешта</b>\n\n"
        for i, post in enumerate(posts, 1):
            text += f"{i}. <b>{post.name}</b>\n"
            text += f"   Категория: {post.category}\n"
            text += f"   Номер: #{post.catalog_number}\n"
            if post.author_username:
                text += f"   Автор: @{post.author_username}\n"
            text += f"   👁 {post.views} просмотров\n\n"
        
        # Update views
        for post in posts:
            post.views += 1
        await session.commit()
        
        await message.answer(text)

@router.message(Command("gorateme"))
async def cmd_gorateme(message: Message, state: FSMContext):
    """Submit to rating - with cooldown check"""
    async for session in get_session():
        can, time_left = await check_cooldown(session, message.from_user.id, 'gorateme')
        
        if not can:
            hours = time_left // 3600
            minutes = (time_left % 3600) // 60
            await message.answer(
                f"⏰ Вы недавно подавали заявку в ТОП\n\n"
                f"Попробуйте через {hours}ч {minutes}мин"
            )
            return
        
        await state.set_state(RatingStates.waiting_for_name)
        await message.answer(
            "⭐ <b>Подать заявку в ТОП</b>\n\n"
            "Шаг 1/5: Введите ваше имя\n\n"
            "Это имя будет показано в рейтинге."
        )

@router.message(RatingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Process rating name"""
    await state.update_data(name=message.text)
    await state.set_state(RatingStates.waiting_for_profile)
    await message.answer(
        "⭐ Шаг 2/5: Ссылка на профиль\n\n"
        "Отправьте ссылку на Instagram или Telegram\n"
        "Или напишите 'пропустить'\n\n"
        "Пример: https://instagram.com/username"
    )

@router.message(RatingStates.waiting_for_profile)
async def process_profile(message: Message, state: FSMContext):
    """Process profile URL"""
    profile = None if message.text.lower() == 'пропустить' else message.text
    await state.update_data(profile_url=profile)
    await state.set_state(RatingStates.waiting_for_about)
    await message.answer(
        "⭐ Шаг 3/5: О себе\n\n"
        "Напишите 3 слова о себе (максимум 7 символов каждое)\n\n"
        "Примеры:\n"
        "модель фото стиль\n"
        "танцы музыка вайб"
    )

@router.message(RatingStates.waiting_for_about)
async def process_about(message: Message, state: FSMContext):
    """Process about - validate 3 words x 7 chars"""
    words = message.text.split()
    
    if len(words) != 3:
        await message.answer("❌ Нужно ровно 3 слова. Попробуйте еще раз:")
        return
    
    if any(len(w) > 7 for w in words):
        await message.answer("❌ Максимум 7 символов на слово. Попробуйте еще раз:")
        return
    
    await state.update_data(about=message.text)
    await state.set_state(RatingStates.waiting_for_gender)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👱🏻‍♀️ Девушка", callback_data="gender:girl"),
            InlineKeyboardButton(text="🤵🏼‍♂️ Парень", callback_data="gender:boy")
        ]
    ])
    await message.answer("⭐ Шаг 4/5: Выберите пол", reply_markup=keyboard)

@router.callback_query(F.data.startswith("gender:"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    """Process gender selection"""
    gender = callback.data.split(":")[1]
    await state.update_data(gender=gender)
    await state.set_state(RatingStates.waiting_for_media)
    await callback.message.answer(
        "⭐ Шаг 5/5: Отправьте фото или видео\n\n"
        "Это будет показано в вашей карточке рейтинга"
    )
    await callback.answer()

@router.message(RatingStates.waiting_for_media, F.photo | F.video)
async def process_media(message: Message, state: FSMContext):
    """Process media and create rating post"""
    data = await state.get_data()
    
    if message.photo:
        media_type = 'photo'
        media_file_id = message.photo[-1].file_id
    else:
        media_type = 'video'
        media_file_id = message.video.file_id
    
    async for session in get_session():
        # Generate catalog number
        catalog_number = await generate_catalog_number(session)
        
        # Create rating post
        post = RatingPost(
            catalog_number=catalog_number,
            name=data['name'],
            profile_url=data.get('profile_url'),
            about=data['about'],
            gender=data['gender'],
            media_type=media_type,
            media_file_id=media_file_id,
            author_user_id=message.from_user.id,
            author_username=message.from_user.username,
            status='pending'
        )
        session.add(post)
        await session.commit()
        
        # Set cooldown (3 hours)
        await set_cooldown(session, message.from_user.id, 'gorateme', 10800)
        
        await message.answer(
            "✅ Заявка отправлена на модерацию!\n\n"
            f"Номер карточки: #{catalog_number}\n\n"
            "Вы получите уведомление когда заявка будет одобрена.\n"
            "После публикации пользователи смогут голосовать за вас!"
        )
    
    await state.clear()

@router.message(Command("toppeople"))
async def cmd_toppeople(message: Message):
    """Show top 10 all"""
    async for session in get_session():
        result = await session.execute(
            select(RatingPost).where(RatingPost.status == 'approved')
            .order_by(RatingPost.total_score.desc()).limit(10)
        )
        posts = result.scalars().all()
        
        if not posts:
            await message.answer("🏆 Рейтинг пока пуст")
            return
        
        text = "🏆 <b>ТОП-10 людей Будапешта</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} <b>{post.name}</b>\n"
            text += f"    Рейтинг: {post.total_score} ({post.vote_count} голосов)\n\n"
        
        await message.answer(text)

@router.message(Command("topboys"))
async def cmd_topboys(message: Message):
    """Show top 10 boys"""
    async for session in get_session():
        result = await session.execute(
            select(RatingPost)
            .where(RatingPost.status == 'approved', RatingPost.gender == 'boy')
            .order_by(RatingPost.total_score.desc()).limit(10)
        )
        posts = result.scalars().all()
        
        if not posts:
            await message.answer("🤵🏼‍♂️ Рейтинг TopBoys пока пуст")
            return
        
        text = "🤵🏼‍♂️ <b>ТОП-10 парней</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} {post.name} - {post.total_score}\n"
        
        await message.answer(text)

@router.message(Command("topgirls"))
async def cmd_topgirls(message: Message):
    """Show top 10 girls"""
    async for session in get_session():
        result = await session.execute(
            select(RatingPost)
            .where(RatingPost.status == 'approved', RatingPost.gender == 'girl')
            .order_by(RatingPost.total_score.desc()).limit(10)
        )
        posts = result.scalars().all()
        
        if not posts:
            await message.answer("👱🏻‍♀️ Рейтинг TopGirls пока пуст")
            return
        
        text = "👱🏻‍♀️ <b>ТОП-10 девушек</b>\n\n"
        medals = ['🥇', '🥈', '🥉']
        for i, post in enumerate(posts):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} {post.name} - {post.total_score}\n"
        
        await message.answer(text)

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Stats command (admin only)"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Только для администраторов")
        return
    
    async for session in get_session():
        users = await session.execute(select(func.count(User.id)))
        total_users = users.scalar_one()
        
        posts = await session.execute(select(func.count(CatalogPost.id)))
        total_posts = posts.scalar_one()
        
        ratings = await session.execute(select(func.count(RatingPost.id)))
        total_ratings = ratings.scalar_one()
        
        await message.answer(
            f"📊 <b>Статистика бота</b>\n\n"
            f"👥 Всего пользователей: {total_users}\n"
            f"📂 Постов в каталоге: {total_posts}\n"
            f"⭐ Рейтинговых постов: {total_ratings}\n"
        )

@router.message(Command("changeuid"))
async def cmd_changeuid(message: Message):
    """Change UID command (admin only)"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Только для администраторов")
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer(
            "❌ Неверный формат\n\n"
            "Используйте: /changeuid <current_uid> <new_uid>\n"
            "Пример: /changeuid 12345 99999"
        )
        return
    
    try:
        current_uid = int(args[1])
        new_uid = int(args[2])
    except ValueError:
        await message.answer("❌ UID должны быть числами")
        return
    
    async for session in get_session():
        # Find user with current UID
        result = await session.execute(select(User).where(User.uid == current_uid))
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer(f"❌ Пользователь с UID {current_uid} не найден")
            return
        
        # Check if new UID is free
        result = await session.execute(select(User).where(User.uid == new_uid))
        if result.scalar_one_or_none():
            await message.answer(f"❌ UID {new_uid} уже занят")
            return
        
        # Check if new UID is not reserved
        if new_uid in RESERVED_UIDS:
            await message.answer(f"❌ UID {new_uid} зарезервирован")
            return
        
        # Change UID
        old_uid = user.uid
        user.uid = new_uid
        await session.commit()
        
        await message.answer(
            f"✅ UID успешно изменен\n\n"
            f"Пользователь: @{user.username}\n"
            f"Старый UID: {old_uid}\n"
            f"Новый UID: {new_uid}"
        )

# ====================== MAIN ======================
async def main():
    """Main function"""
    print("🚀 Starting TrixBot...")
    print(f"Admin IDs: {ADMIN_IDS}")
    
    # Initialize database
    await init_db()
    
    # Register router
    dp.include_router(router)
    
    # Get bot info
    me = await bot.get_me()
    print(f"✅ Bot started: @{me.username} (ID: {me.id})")
    
    # Start polling
    print("📡 Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
