from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from bot.keyboards.inline import main_menu

router = Router()

WELCOME_TEXT = """
👋 Привет, {name}!

Добро пожаловать в <b>BarberBoss Bishkek</b> ✂️

Мы — современный барбершоп в сердце Бишкека.
Лучшие мастера, стильные стрижки, приятная атмосфера.

Выбери что тебя интересует 👇
"""


@router.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name or "Друг"
    await message.answer(
        WELCOME_TEXT.format(name=name),
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "menu")
async def back_to_menu(call: CallbackQuery):
    name = call.from_user.first_name or "Друг"
    await call.message.edit_text(
        WELCOME_TEXT.format(name=name),
        parse_mode="HTML",
        reply_markup=main_menu(),
    )
