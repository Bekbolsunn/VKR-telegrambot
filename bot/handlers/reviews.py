from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu

router = Router()


@router.callback_query(F.data.startswith("review_"))
async def handle_review(call: CallbackQuery):
    parts = call.data.split("_")
    rating = int(parts[2])
    stars = "⭐" * rating
    messages = {
        1: "Жаль это слышать 😔 Мы обязательно улучшимся!",
        2: "Спасибо за честность. Передадим мастеру.",
        3: "Спасибо! Будем стараться лучше 💪",
        4: "Отлично! Рады что понравилось 😊",
        5: "Вау! Ты лучший клиент! 🔥 Ждём снова!",
    }
    await call.message.edit_text(
        f"<b>Твоя оценка: {stars}</b>\n\n"
        f"{messages[rating]}\n\n"
        "🏆 +100 баллов лояльности начислено за отзыв!",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
