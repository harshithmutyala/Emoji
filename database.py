import aiosqlite

DB_PATH = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            emoji_count INTEGER DEFAULT 0,
            pack_count INTEGER DEFAULT 0
        )
        """)
        await db.commit()


async def update_user(user_id, username, emojis=0, packs=0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT INTO users (user_id, username, emoji_count, pack_count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            emoji_count = emoji_count + excluded.emoji_count,
            pack_count = pack_count + excluded.pack_count
        """, (user_id, username, emojis, packs))
        await db.commit()
