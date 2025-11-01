from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from CORE.states import RatingCreationStates

router = Router(name='rating_callbacks')

@router.callback_query(F.data.startswith("gender:"))
async def process_gender_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора пола через кнопку"""
    gender = callback.data.split(":")[1]
    
    await state.update_data(gender=gender)
    await state.set_state(RatingCreationStates.waiting_for_media)
    
    await callback.message.answer(
        "⭐ Шаг 5/5: Отправьте фото или видео\n\n"
        "Это будет показано в вашей карточке рейтинга"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("vote:"))
async def process_vote_callback(callback: CallbackQuery):
    """Обработка голосования"""
    from DATABASE.base import get_session
    from SERVICES.database.rating_service import RatingService
    
    parts = callback.data.split(":")
    rating_post_id = int(parts[1])
    vote_value = int(parts[2])
    
    async for session in get_session():
        success, message = await RatingService.vote_for_post(
            session, rating_post_id, callback.from_user.id, vote_value
        )
        
        if success:
            await callback.answer(f"✅ Ваш голос: {vote_value:+d}", show_alert=True)
        else:
            await callback.answer(f"❌ {message}", show_alert=True)

@router.callback_query(F.data.startswith("mod_"))
async def process_moderation_callback(callback: CallbackQuery):
    """Обработка модерации заявок"""
    from CORE.config import settings
    
    if not settings.is_admin(callback.from_user.id):
        await callback.answer("❌ Недостаточно прав", show_alert=True)
        return
    
    action = callback.data.split("_")[1].split(":")[0]
    
    if action == "approve":
        await callback.answer("✅ Заявка одобрена", show_alert=True)
        # TODO: Реализовать публикацию
    elif action == "reject":
        await callback.answer("❌ Заявка отклонена", show_alert=True)
        # TODO: Реализовать отклонение
    elif action == "edit":
        await callback.answer("✏️ Редактирование", show_alert=True)
        # TODO: Реализовать редактирование
