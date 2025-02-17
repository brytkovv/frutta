import asyncio

from vkbottle import Bot
import uvloop

from app.config import BOT_TOKEN
from app.handlers.admin import admin_labeler
from app.handlers.user import user_labeler
from app.handlers.menu import menu_labeler
from app.database import init_db
from app.redis_cache import init_redis
from app.localization import load_locale


async def main():
    await init_db()
    await init_redis()
    load_locale()

    bot = Bot(token=BOT_TOKEN)

    admin_labeler.load(bot)
    user_labeler.load(bot)
    menu_labeler.load(bot)

    await bot.run_polling()


if __name__ == "__main__":
    # uvloop обычно даёт выигрыш в производительности на Unix системах
    uvloop.install()
    asyncio.run(main())
