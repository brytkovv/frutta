from vkbottle.bot import Blueprint, Message
from app.localization import get_locale
from app.utils.keyboards import main_menu_keyboard
from app.config import VK_ADMIN_IDS

menu_bp = Blueprint(name="menu_blueprint")

@menu_bp.on.message(text=["Назад", "назад", "<back>", "/start", "start"])  # Возможные варианты
@menu_bp.on.message(payload={"cmd": "back"})  # если используем payload
async def back_to_menu(message: Message):
    # Просто отправим приветственное сообщение + главное меню
    greetings = get_locale("text.greetings")
    await message.answer(
        greetings,
        keyboard=main_menu_keyboard().get_json()
    )

@menu_bp.on.message(text=["Привет", "Начать", "Старт"])  # или любой триггер
async def greet_user(message: Message):
    # Тот же код, что и при "назад"
    greetings = get_locale("text.greetings")
    await message.answer(
        greetings,
        keyboard=main_menu_keyboard().get_json()
    )

# (Если хотим, можем отдельную кнопку "Админка" в main_menu_keyboard(),
#  тогда здесь тоже можно отловить.)
@menu_bp.on.message(text=["Админка", "админка"])
async def admin_panel_entry(message: Message):
    # Если user_id не в VK_ADMIN_IDS, отвергаем
    if message.from_id not in VK_ADMIN_IDS:
        await message.answer("Недостаточно прав.")
        return

    # иначе перенаправим куда-нибудь (допустим, в хендлер из admin.py)
    # Можно сразу вызвать хендлер или отправить своё сообщение
    from app.handlers.admin import show_admin_menu
    await show_admin_menu(message)
