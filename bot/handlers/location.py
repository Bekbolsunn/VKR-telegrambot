from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import SHOP_LOCATION
from bot.keyboards.inline import back_to_menu

router = Router()


@router.callback_query(F.data == "location")
async def show_location(call: CallbackQuery):
    loc = SHOP_LOCATION
    await call.message.edit_text(
        "📍 <b>Как добраться</b>\n\n"
        f"🏠 {loc['address']}\n"
        f"{loc['metro']}\n"
        f"🕐 {loc['hours']}\n\n"
        "🗺 Координаты для навигатора:\n"
        f"<code>{loc['lat']}, {loc['lon']}</code>\n\n"
        "📲 Открой в:\n"
        "• 2GIS: 2gis.kg → BarberBoss\n"
        "• Google Maps: поиск «BarberBoss Bishkek»\n"
        "• Яндекс.Карты: поиск «BarberBoss»",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
