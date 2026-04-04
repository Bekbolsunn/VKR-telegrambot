import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-ngrok-url.ngrok-free.app")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp  = Dispatcher()


def webapp_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="✂️ Открыть BarberBoss",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])


@dp.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name or "Друг"
    await message.answer(
        f"👋 Привет, <b>{name}</b>!\n\n"
        "Добро пожаловать в <b>BarberBoss Bishkek</b> ✂️\n\n"
        "Нажми кнопку ниже чтобы записаться,\n"
        "посмотреть прайс и акции 👇",
        reply_markup=webapp_keyboard(),
    )


@dp.message(F.web_app_data)
async def on_webapp_data(message: Message):
    """Получение данных из WebApp (для будущей интеграции)"""
    await message.answer(f"📩 Получены данные: {message.web_app_data.data}")


async def main():
    logging.info("🚀 BarberBoss Bot запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
