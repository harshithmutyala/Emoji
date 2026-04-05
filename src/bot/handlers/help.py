from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    text = (
        "<b>📖 Help Menu</b>\n\n"
        "• Send emoji → get ID\n"
        "• Send pack link → get all IDs\n\n"
        "<i>Powered by BotOrigin 🚀</i>"
    )
    await message.answer(text)
