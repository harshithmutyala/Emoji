import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from config import BOT_TOKEN
from database import init_db, update_user

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await update_user(message.from_user.id, message.from_user.username)

    text = (
        "<b>👋 Welcome to Emoji ID Bot</b>\n\n"
        "Send any custom emoji or emoji pack link.\n"
        "I will give you emoji IDs instantly ⚡\n\n"
        "<i>Powered by BotOrigin 🚀</i>"
    )
    await message.answer(text)


@dp.message(F.text)
async def handle(message: types.Message):
    text = message.text.strip()

    # Handle emoji pack
    if "addemoji/" in text:
        pack_name = text.split("addemoji/")[-1].split("?")[0]

        try:
            sticker_set = await bot.get_sticker_set(pack_name)

            msg = f"📦 <b>{sticker_set.title}</b>\n"
            msg += f"🔢 Total: {len(sticker_set.stickers)}\n\n"

            count = 0

            for i, s in enumerate(sticker_set.stickers, 1):
                if not s.custom_emoji_id:
                    continue

                count += 1
                emoji = s.emoji or "❓"

                msg += f"{i}. <code>{emoji}</code> → <code>{s.custom_emoji_id}</code>\n"

                if len(msg) > 3500:
                    await message.answer(msg)
                    msg = ""

            if msg:
                await message.answer(msg)

            await update_user(message.from_user.id, message.from_user.username, packs=1)

        except Exception as e:
            await message.reply(f"❌ Error: <code>{e}</code>")

        return

    # Handle custom emoji
    if message.entities:
        emojis = [e for e in message.entities if e.type == "custom_emoji"]

        if emojis:
            res = []
            for e in emojis:
                emoji_id = e.custom_emoji_id
                original = e.extract_from(message.text)

                res.append(f"<code>{original}</code> → <code>{emoji_id}</code>")

            await update_user(
                message.from_user.id,
                message.from_user.username,
                emojis=len(res)
            )

            await message.reply("\n".join(res))


async def main():
    await init_db()
    print("🚀 Bot started | Powered by BotOrigin")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
