import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
)
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-ngrok-url.ngrok-free.app")
ADMIN_ID   = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp  = Dispatcher()


def reply_keyboard() -> ReplyKeyboardMarkup:
    """Постоянная кнопка снизу экрана — открывает WebApp."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✂️ Записаться / Открыть", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
        persistent=True,
    )


@dp.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name or "Друг"
    await message.answer(
        f"👋 Привет, <b>{name}</b>!\n\n"
        "Добро пожаловать в <b>BarberBoss Bishkek</b> ✂️\n\n"
        "Нажми кнопку ниже чтобы записаться,\n"
        "посмотреть прайс и акции 👇",
        reply_markup=reply_keyboard(),
    )


@dp.message(F.web_app_data)
async def on_webapp_data(message: Message):
    await message.answer(f"📩 Получены данные: {message.web_app_data.data}")


async def main():
    logging.info("🚀 BarberBoss Bot запущен!")
    await bot.delete_webhook(drop_pending_updates=True)

    if ADMIN_ID:
        try:
            await bot.send_message(
                ADMIN_ID,
                "✅ <b>BarberBoss Bot запущен</b>\n\n"
                f"🌐 WebApp: {WEBAPP_URL}\n"
                "📊 Всё работает нормально",
            )
        except Exception as e:
            logging.warning(f"Не удалось отправить уведомление админу: {e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
