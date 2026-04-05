from aiogram import types
from aiogram import Bot

bot = Bot.get_current()


async def process_message(message: types.Message):
    text = message.text.strip()

    # Handle pack
    if "addemoji/" in text:
        pack_name = text.split("addemoji/")[-1].split("?")[0]

        try:
            sticker_set = await bot.get_sticker_set(pack_name)

            msg = f"📦 <b>{sticker_set.title}</b>\n"
            msg += f"🔢 Total: {len(sticker_set.stickers)}\n\n"

            for i, s in enumerate(sticker_set.stickers, 1):
                if not s.custom_emoji_id:
                    continue

                emoji = s.emoji or "❓"
                msg += f"{i}. <code>{emoji}</code> → <code>{s.custom_emoji_id}</code>\n"

                if len(msg) > 3500:
                    return msg

            return msg

        except Exception as e:
            return f"❌ Error: <code>{e}</code>"

    # Handle custom emoji
    if message.entities:
        emojis = [e for e in message.entities if e.type == "custom_emoji"]

        if emojis:
            res = []
            for e in emojis:
                emoji_id = e.custom_emoji_id
                original = e.extract_from(message.text)

                res.append(f"<code>{original}</code> → <code>{emoji_id}</code>")

            return "\n".join(res)

    return None
