from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import BARBERS, SERVICES, ALL_SLOTS, BUSY_SLOTS
from bot.keyboards.inline import (
    barbers_kb, dates_kb, slots_kb, services_kb, confirm_kb,
    after_booking_kb, payment_kb,
)

router = Router()


@router.callback_query(F.data == "book_start")
async def book_start(call: CallbackQuery):
    await call.message.edit_text(
        "<b>✂️ Выбери мастера</b>\n\nВсе наши барберы — профессионалы своего дела 👇",
        parse_mode="HTML",
        reply_markup=barbers_kb(BARBERS),
    )


@router.callback_query(F.data.startswith("barber_"))
async def choose_barber(call: CallbackQuery):
    barber_id = int(call.data.split("_")[1])
    barber = next(b for b in BARBERS if b["id"] == barber_id)
    await call.message.edit_text(
        f"<b>{barber['emoji']} {barber['name']}</b>\n"
        f"Специализация: {barber['spec']}\n"
        f"Рейтинг: {barber['rating']}\n\n"
        f"📅 Выбери удобный день:",
        parse_mode="HTML",
        reply_markup=dates_kb(barber_id),
    )


@router.callback_query(F.data.startswith("date_"))
async def choose_date(call: CallbackQuery):
    _, barber_id, date_str = call.data.split("_", 2)
    busy = BUSY_SLOTS.get(barber_id, {}).get(date_str, [])
    free = len(ALL_SLOTS) - len(busy)
    await call.message.edit_text(
        f"📅 <b>{date_str}</b>\n\n"
        f"🟢 Свободно слотов: <b>{free}</b>\n"
        f"❌ — занято  |  🕐 — свободно\n\n"
        f"Выбери удобное время:",
        parse_mode="HTML",
        reply_markup=slots_kb(barber_id, date_str, ALL_SLOTS, busy),
    )


@router.callback_query(F.data == "slot_busy")
async def slot_busy(call: CallbackQuery):
    await call.answer("❌ Этот слот уже занят, выбери другое время", show_alert=True)


@router.callback_query(F.data.startswith("slot_"))
async def choose_slot(call: CallbackQuery):
    parts = call.data.split("_")
    barber_id, date_str, time_str = parts[1], parts[2], parts[3]
    await call.message.edit_text(
        f"🕐 <b>Время: {time_str}</b>\n"
        f"📅 Дата: {date_str}\n\n"
        f"💈 Выбери услугу:",
        parse_mode="HTML",
        reply_markup=services_kb(barber_id, date_str, time_str, SERVICES),
    )


@router.callback_query(F.data.startswith("svc_"))
async def choose_service(call: CallbackQuery):
    parts = call.data.split("_")
    barber_id, date_str, time_str, svc_id = parts[1], parts[2], parts[3], parts[4]
    barber = next(b for b in BARBERS if b["id"] == int(barber_id))
    service = next(s for s in SERVICES if s["id"] == int(svc_id))
    await call.message.edit_text(
        "📋 <b>Подтверди запись</b>\n\n"
        f"👨‍💈 Мастер:  {barber['name']}\n"
        f"✂️ Услуга:  {service['name']}\n"
        f"📅 Дата:    {date_str}\n"
        f"🕐 Время:   {time_str}\n"
        f"💵 Цена:    {service['price']} сом\n"
        f"⏱ Длит.:   {service['duration']}\n\n"
        "Всё верно?",
        parse_mode="HTML",
        reply_markup=confirm_kb(barber_id, date_str, time_str, svc_id),
    )


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_booking(call: CallbackQuery):
    parts = call.data.split("_")
    barber_id, date_str, time_str, svc_id = parts[1], parts[2], parts[3], parts[4]
    barber = next(b for b in BARBERS if b["id"] == int(barber_id))
    service = next(s for s in SERVICES if s["id"] == int(svc_id))
    await call.message.edit_text(
        "🎉 <b>Запись подтверждена!</b>\n\n"
        f"👨‍💈 {barber['name']}\n"
        f"✂️ {service['name']}\n"
        f"📅 {date_str}  🕐 {time_str}\n"
        f"💵 {service['price']} сом\n\n"
        "⏰ Напомним за 24 часа до визита!\n\n"
        "💳 Хочешь оплатить предоплату 200 сом\n"
        "через мобильный банк?",
        parse_mode="HTML",
        reply_markup=after_booking_kb(),
    )


@router.callback_query(F.data == "pay_mbank")
async def pay_mbank(call: CallbackQuery):
    await call.message.edit_text(
        "💳 <b>Выбери способ оплаты</b>\n\n"
        "Предоплата: <b>200 сом</b>\n"
        "После оплаты отправь скриншот сюда 👇",
        parse_mode="HTML",
        reply_markup=payment_kb(),
    )


@router.callback_query(F.data.startswith("pay_detail_"))
async def pay_detail(call: CallbackQuery):
    method = call.data.split("_")[2]
    from bot.config import MBANK_DETAILS
    details = {
        "mbank": ("🟢 Mbank",  MBANK_DETAILS["mbank"]),
        "opay":  ("🔵 O!Pay",  MBANK_DETAILS["opay"]),
        "elsom": ("🟣 Elsom",  MBANK_DETAILS["elsom"]),
    }
    name, phone = details[method]
    from bot.keyboards.inline import back_to_menu
    await call.message.edit_text(
        f"<b>{name}</b>\n\n"
        f"📱 Номер: <code>{phone}</code>\n"
        f"💵 Сумма: <b>200 сом</b>\n\n"
        "1. Переведи 200 сом на этот номер\n"
        "2. Сделай скриншот перевода\n"
        "3. Отправь скриншот в этот чат\n\n"
        "✅ Администратор подтвердит в течение 15 минут",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )


@router.callback_query(F.data == "pay_cash")
async def pay_cash(call: CallbackQuery):
    from bot.keyboards.inline import back_to_menu
    await call.message.edit_text(
        "💵 <b>Оплата на месте</b>\n\n"
        "Отлично! Оплатишь при визите.\n\n"
        "⚠️ Просьба предупредить за 2 часа\n"
        "если не сможешь прийти.\n\n"
        "До встречи! 💈",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
