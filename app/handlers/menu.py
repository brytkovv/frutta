from vkbottle.bot import Blueprint, Message
from app.localization import get_locale
from app.utils.keyboards import main_menu_keyboard
from app.config import VK_ADMIN_IDS


menu_labeler = Blueprint()
menu_labeler.vbml_ignore_case = True  # Игнорируем регистр команд


@menu_labeler.on.message(text=["Назад", "Назад в меню", "/start", "start", "Привет", "Начать", "Старт"]) # get_locale("button.back")
@menu_labeler.on.message(payload={"cmd": "back"})
async def back_to_menu(message: Message):
    greetings = get_locale("text.greetings")
    await message.answer(greetings, keyboard=main_menu_keyboard().get_json())


@menu_labeler.on.message(text=["Админка", "админка"]) #  get_locale("button.admin")
async def admin_panel_entry(message: Message):
    if message.from_id not in VK_ADMIN_IDS:
        return

    from app.handlers.admin import show_admin_menu
    await show_admin_menu(message)
