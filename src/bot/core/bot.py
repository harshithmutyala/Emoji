import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from src.bot.handlers import start, help, message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def register_handlers():
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(message.router)


async def start_bot():
    register_handlers()
    print("🚀 Bot started | Powered by BotOrigin")
    await dp.start_polling(bot)
