from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💰 Прайс",           callback_data="price"),
        InlineKeyboardButton(text="✂️ Записаться",      callback_data="book_start"),
    )
    builder.row(
        InlineKeyboardButton(text="📋 Мои записи",      callback_data="my_bookings"),
        InlineKeyboardButton(text="🎁 Акции",           callback_data="promos"),
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Мои баллы",       callback_data="loyalty"),
        InlineKeyboardButton(text="📸 Галерея",         callback_data="gallery"),
    )
    builder.row(
        InlineKeyboardButton(text="📍 Как добраться",   callback_data="location"),
        InlineKeyboardButton(text="👥 Реферал",         callback_data="referral"),
    )
    return builder.as_markup()


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu")
    ]])


def barbers_kb(barbers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in barbers:
        builder.row(InlineKeyboardButton(
            text=f"{b['emoji']} {b['name']}  {b['rating']}",
            callback_data=f"barber_{b['id']}"
        ))
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="menu"))
    return builder.as_markup()


def dates_kb(barber_id: int) -> InlineKeyboardMarkup:
    from datetime import date, timedelta
    builder = InlineKeyboardBuilder()
    today = date.today()
    days_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for i in range(7):
        d = today + timedelta(days=i)
        label = "Сегодня" if i == 0 else ("Завтра" if i == 1 else f"{days_ru[d.weekday()]} {d.day} мар")
        builder.button(
            text=label,
            callback_data=f"date_{barber_id}_{d.isoformat()}"
        )
    builder.adjust(3)
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="book_start"))
    return builder.as_markup()


def slots_kb(barber_id: int, date_str: str, all_slots: list, busy: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for slot in all_slots:
        if slot in busy:
            builder.button(text=f"❌ {slot}", callback_data="slot_busy")
        else:
            builder.button(text=f"🕐 {slot}", callback_data=f"slot_{barber_id}_{date_str}_{slot}")
    builder.adjust(4)
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data=f"barber_{barber_id}"))
    return builder.as_markup()


def services_kb(barber_id: str, date_str: str, time_str: str, services: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for s in services:
        builder.row(InlineKeyboardButton(
            text=f"{s['name']} — {s['price']} сом ({s['duration']})",
            callback_data=f"svc_{barber_id}_{date_str}_{time_str}_{s['id']}"
        ))
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data=f"date_{barber_id}_{date_str}"))
    return builder.as_markup()


def confirm_kb(barber_id: str, date_str: str, time_str: str, svc_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Подтвердить",  callback_data=f"confirm_{barber_id}_{date_str}_{time_str}_{svc_id}"),
        InlineKeyboardButton(text="❌ Отмена",       callback_data="menu"),
    )
    return builder.as_markup()


def after_booking_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💳 Оплатить предоплату (Mbank)", callback_data="pay_mbank"))
    builder.row(InlineKeyboardButton(text="💵 Оплачу на месте",            callback_data="pay_cash"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню",               callback_data="menu"))
    return builder.as_markup()


def payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🟢 Mbank",   callback_data="pay_detail_mbank"),
        InlineKeyboardButton(text="🔵 O!Pay",   callback_data="pay_detail_opay"),
        InlineKeyboardButton(text="🟣 Elsom",   callback_data="pay_detail_elsom"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="menu"))
    return builder.as_markup()


def my_bookings_kb(bookings: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in bookings:
        builder.row(InlineKeyboardButton(
            text=f"✂️ {b['date']} {b['time']} — {b['barber']}",
            callback_data=f"view_booking_{b['id']}"
        ))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    return builder.as_markup()


def booking_detail_kb(booking_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Отменить запись", callback_data=f"cancel_booking_{booking_id}"))
    builder.row(InlineKeyboardButton(text="◀️ Назад",           callback_data="my_bookings"))
    return builder.as_markup()


def promos_kb(promos: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in promos:
        builder.row(InlineKeyboardButton(
            text=f"{p['emoji']} {p['title']}",
            callback_data=f"promo_{p['id']}"
        ))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    return builder.as_markup()


def promo_detail_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✂️ Записаться со скидкой", callback_data="book_start"))
    builder.row(InlineKeyboardButton(text="◀️ Акции",                 callback_data="promos"))
    return builder.as_markup()


def gallery_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✂️ Классика",     callback_data="gal_classic"),
        InlineKeyboardButton(text="💈 Фейд",          callback_data="gal_fade"),
    )
    builder.row(
        InlineKeyboardButton(text="🪒 Борода",        callback_data="gal_beard"),
        InlineKeyboardButton(text="🎨 Дизайн",        callback_data="gal_design"),
    )
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    return builder.as_markup()


def loyalty_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎁 Потратить баллы",      callback_data="spend_points"))
    builder.row(InlineKeyboardButton(text="📜 История начислений",   callback_data="points_history"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню",         callback_data="menu"))
    return builder.as_markup()


def review_kb(booking_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, star in enumerate(["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], 1):
        builder.button(text=star, callback_data=f"review_{booking_id}_{i}")
    builder.adjust(5)
    builder.row(InlineKeyboardButton(text="Пропустить", callback_data="menu"))
    return builder.as_markup()
