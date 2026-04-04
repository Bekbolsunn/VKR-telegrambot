from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import PROMOTIONS
from bot.keyboards.inline import promos_kb, promo_detail_kb

router = Router()


@router.callback_query(F.data == "promos")
async def show_promos(call: CallbackQuery):
    await call.message.edit_text(
        "🎁 <b>Акции и скидки</b>\n\n"
        "🇰🇬 Специальные предложения для наших клиентов!\n\n"
        "Выбери акцию чтобы узнать подробности 👇",
        parse_mode="HTML",
        reply_markup=promos_kb(PROMOTIONS),
    )


@router.callback_query(F.data.startswith("promo_"))
async def show_promo_detail(call: CallbackQuery):
    promo_id = int(call.data.split("_")[1])
    promo = next((p for p in PROMOTIONS if p["id"] == promo_id), None)
    if not promo:
        await call.answer("Акция не найдена", show_alert=True)
        return

    await call.message.edit_text(
        f"{promo['emoji']} <b>{promo['title']}</b>\n\n"
        f"{promo['desc']}\n\n"
        f"🗓 Срок: {promo['until']}\n"
        f"🎟 Промокод: <code>{promo['code']}</code>\n\n"
        "Скопируй промокод и назови его при записи!",
        parse_mode="HTML",
        reply_markup=promo_detail_kb(),
    )
