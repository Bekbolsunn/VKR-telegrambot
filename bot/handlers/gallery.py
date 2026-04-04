from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import gallery_kb, back_to_menu

router = Router()

GALLERY_ITEMS = {
    "gal_classic": {
        "title": "✂️ Классика",
        "desc": (
            "Классическая мужская стрижка — вечный стиль.\n\n"
            "• Аккуратные виски\n"
            "• Чёткий контур\n"
            "• Укладка помадой или глиной\n\n"
            "💵 От 350 сом  |  ⏱ 45 мин"
        ),
    },
    "gal_fade": {
        "title": "💈 Фейд (Fade)",
        "desc": (
            "Плавный переход от кожи до длины — самый популярный стиль.\n\n"
            "• Skin Fade — до нуля\n"
            "• Low / Mid / High Fade\n"
            "• Идеально для любого типа волос\n\n"
            "💵 От 450 сом  |  ⏱ 50 мин"
        ),
    },
    "gal_beard": {
        "title": "🪒 Борода",
        "desc": (
            "Оформление и моделирование бороды.\n\n"
            "• Чёткий контур\n"
            "• Выравнивание длины\n"
            "• Горячее полотенце + масло для бороды\n\n"
            "💵 От 250 сом  |  ⏱ 30 мин"
        ),
    },
    "gal_design": {
        "title": "🎨 Дизайн",
        "desc": (
            "Авторские дизайны и узоры — выдели себя из толпы.\n\n"
            "• Геометрические узоры\n"
            "• Надписи и линии\n"
            "• Любая сложность по договорённости\n\n"
            "💵 От 500 сом  |  ⏱ 60 мин"
        ),
    },
}


@router.callback_query(F.data == "gallery")
async def show_gallery(call: CallbackQuery):
    await call.message.edit_text(
        "📸 <b>Галерея стрижек</b>\n\n"
        "Выбери стиль чтобы узнать подробности\n"
        "и найти референс для своего мастера 👇",
        parse_mode="HTML",
        reply_markup=gallery_kb(),
    )


@router.callback_query(F.data.startswith("gal_"))
async def show_gallery_item(call: CallbackQuery):
    item = GALLERY_ITEMS.get(call.data)
    if not item:
        await call.answer("Не найдено", show_alert=True)
        return
    await call.message.edit_text(
        f"<b>{item['title']}</b>\n\n{item['desc']}",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
