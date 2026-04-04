from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import MY_BOOKINGS
from bot.keyboards.inline import my_bookings_kb, booking_detail_kb, back_to_menu

router = Router()


@router.callback_query(F.data == "my_bookings")
async def show_my_bookings(call: CallbackQuery):
    if not MY_BOOKINGS:
        await call.message.edit_text(
            "📋 <b>Мои записи</b>\n\nУ тебя пока нет активных записей.\n\n"
            "Нажми «Записаться» чтобы забронировать время 💈",
            parse_mode="HTML",
            reply_markup=back_to_menu(),
        )
        return

    await call.message.edit_text(
        f"📋 <b>Мои записи</b>\n\nАктивных записей: {len(MY_BOOKINGS)}\n\nВыбери запись для деталей:",
        parse_mode="HTML",
        reply_markup=my_bookings_kb(MY_BOOKINGS),
    )


@router.callback_query(F.data.startswith("view_booking_"))
async def view_booking(call: CallbackQuery):
    booking_id = int(call.data.split("_")[2])
    b = next((x for x in MY_BOOKINGS if x["id"] == booking_id), None)
    if not b:
        await call.answer("Запись не найдена", show_alert=True)
        return

    await call.message.edit_text(
        f"📋 <b>Детали записи</b>\n\n"
        f"👨‍💈 Мастер:  {b['barber']}\n"
        f"✂️ Услуга:  {b['service']}\n"
        f"📅 Дата:    {b['date']}\n"
        f"🕐 Время:   {b['time']}\n"
        f"💵 Цена:    {b['price']} сом\n"
        f"📌 Статус:  {b['status']}\n\n"
        "Хочешь отменить запись?",
        parse_mode="HTML",
        reply_markup=booking_detail_kb(booking_id),
    )


@router.callback_query(F.data.startswith("cancel_booking_"))
async def cancel_booking(call: CallbackQuery):
    await call.message.edit_text(
        "✅ <b>Запись отменена</b>\n\n"
        "Слот освобождён. Барбер уведомлён.\n\n"
        "Будем ждать тебя снова! 💈",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
