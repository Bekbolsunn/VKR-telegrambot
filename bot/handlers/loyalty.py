from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import LOYALTY_INFO, REFERRAL_INFO
from bot.keyboards.inline import loyalty_kb, back_to_menu

router = Router()


@router.callback_query(F.data == "loyalty")
async def show_loyalty(call: CallbackQuery):
    info = LOYALTY_INFO
    bar_filled = int(info["points"] / (info["points"] + info["points_to_next"]) * 10)
    progress = "🟩" * bar_filled + "⬜" * (10 - bar_filled)

    await call.message.edit_text(
        "🏆 <b>Моя программа лояльности</b>\n\n"
        f"💎 Уровень: {info['level']}\n"
        f"⭐ Баллов: <b>{info['points']}</b>\n\n"
        f"До уровня {info['next_level']}:\n"
        f"{progress} {info['points_to_next']} баллов\n\n"
        "📌 <b>Как копить баллы?</b>\n"
        "• 1 сом = 1 балл\n"
        "• +50 баллов за первый визит\n"
        "• +100 баллов за отзыв\n"
        "• +150 баллов за реферала\n\n"
        "🎁 <b>Как тратить?</b>\n"
        "• 100 баллов = скидка 50 сом",
        parse_mode="HTML",
        reply_markup=loyalty_kb(),
    )


@router.callback_query(F.data == "spend_points")
async def spend_points(call: CallbackQuery):
    info = LOYALTY_INFO
    discounts = info["points"] // 100
    await call.message.edit_text(
        "🎁 <b>Потратить баллы</b>\n\n"
        f"У тебя <b>{info['points']}</b> баллов\n"
        f"Можешь получить скидку: <b>{discounts * 50} сом</b>\n\n"
        "Назови свой Telegram при записи —\n"
        "скидка применится автоматически! ✅",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )


@router.callback_query(F.data == "points_history")
async def points_history(call: CallbackQuery):
    info = LOYALTY_INFO
    lines = ["📜 <b>История баллов</b>\n"]
    for h in info["history"]:
        lines.append(f"• {h['date']}  {h['action']}\n  <b>{h['points']} баллов</b>")
    await call.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )


@router.callback_query(F.data == "referral")
async def show_referral(call: CallbackQuery):
    ref = REFERRAL_INFO
    await call.message.edit_text(
        "👥 <b>Реферальная программа</b>\n\n"
        f"Твой код: <code>{ref['code']}</code>\n\n"
        "📲 Поделись кодом с другом:\n"
        "• Друг получит скидку <b>10%</b> на первый визит\n"
        "• Ты получишь <b>+150 баллов</b>\n\n"
        f"✅ Уже пригласил: <b>{ref['invited']}</b> друга\n"
        f"💰 Заработал: <b>{ref['earned']}</b> баллов\n\n"
        "Отправь код другу прямо сейчас! 🚀",
        parse_mode="HTML",
        reply_markup=back_to_menu(),
    )
