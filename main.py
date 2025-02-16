import asyncio

from vkbottle import Bot
import uvloop

from app.config import BOT_TOKEN, GROUP_ID
from app.handlers.admin import admin_bp
from app.handlers.user import user_bp
from app.handlers.menu import menu_bp
from app.database import init_db
from app.redis_cache import init_redis
from app.localization import load_locale


async def main():
    # Инициализация базы, миграции и т.д.
    await init_db()
    await init_redis()
    load_locale()

    # Создаем экземпляр бота
    bot = Bot(token=BOT_TOKEN, group_id=GROUP_ID)

    # Регистрируем Blueprint'ы
    bot.labeler.load(admin_bp)
    bot.labeler.load(user_bp)
    bot.labeler.load(menu_bp)

    # Запуск бота
    await bot.run_polling()


if __name__ == "__main__":
    # uvloop обычно даёт выигрыш в производительности на Unix системах
    uvloop.install()
    asyncio.run(main())
