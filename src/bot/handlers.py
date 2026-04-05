from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "<b>👋 Welcome to Emoji ID Bot</b>\n\n"
        "Send custom emoji or pack link.\n\n"
        "<i>Powered by BotOrigin 🚀</i>"
    )
    await message.answer(text)
