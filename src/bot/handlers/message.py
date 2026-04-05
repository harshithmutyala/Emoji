from aiogram import Router, types, F
from src.bot.services.reply_service import process_message

router = Router()


@router.message(F.text)
async def handle_message(message: types.Message):
    response = await process_message(message)

    if response:
        await message.reply(response)
