from datetime import datetime

from vkbottle.bot import Blueprint, Message
from app.localization import get_locale
from app.utils.keyboards import main_menu_keyboard
from app.utils.logs import logger


menu_labeler = Blueprint()
menu_labeler.vbml_ignore_case = True  # Игнорируем регистр команд


@menu_labeler.on.message(text=["Назад", "Назад в меню", "Меню", "/start", "start", "Привет", "Начать", "Старт"]) # get_locale("button.back")
@menu_labeler.on.message(payload={"cmd": "back"})
async def back_to_menu(message: Message):
    logger.info(
        f"[{datetime.now()}] back_to_menu handler вызван. user_id={message.from_id}, text={message.text!r}"
    )

    greetings = get_locale("text.greetings")
    await message.answer(greetings, keyboard=main_menu_keyboard().get_json())
