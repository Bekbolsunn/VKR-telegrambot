from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import SERVICES
from bot.keyboards.inline import back_to_menu

router = Router()


@router.callback_query(F.data == "price")
async def show_price(call: CallbackQuery):
    lines = ["<b>💰 Прайс-лист BarberBoss Bishkek</b>\n"]
    for s in SERVICES:
        lines.append(f"✂️ <b>{s['name']}</b>")
        lines.append(f"   💵 {s['price']} сом  |  ⏱ {s['duration']}\n")
    lines.append("📍 Все цены указаны в сомах (KGS)")
    await call.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
