from vkbottle.bot import BotLabeler, Message
from app.localization import get_locale
from app.utils.keyboards import main_menu_keyboard
from app.config import VK_ADMIN_IDS
from vkbottle import Text


menu_labeler = BotLabeler()
menu_labeler.vbml_ignore_case = True  # Игнорируем регистр команд


@menu_labeler.message(text=["Назад", get_locale("button.back"), "/start", "start", "Привет", "Начать", "Старт"])
@menu_labeler.message(payload={"cmd": "back"})
async def back_to_menu(message: Message):
    greetings = get_locale("text.greetings")
    await message.answer(
        greetings,
        keyboard=main_menu_keyboard().get_json()
    )


@menu_labeler.message(text=["Админка", "админка", get_locale("button.admin")])
async def admin_panel_entry(message: Message):
    if message.from_id not in VK_ADMIN_IDS:
        return

    from app.handlers.admin import show_admin_menu
    await show_admin_menu(message)
