import logging
from vkbottle.bot import BotLabeler, Message
from app.services.answers_service import get_answer_by_key
from app.utils.keyboards import back_menu_keyboard, presents_keyboard
from app.localization import get_locale


user_labeler = BotLabeler()
user_labeler.vbml_ignore_case = True  # Игнорируем регистр


@user_labeler.message(text=["Акции", "Актуальные акции и предложения"]) # get_locale("button.home_page.stock")
async def handle_stock(message: Message):
    logging.info(f"handle_stock called by user_id={message.from_id}, text={message.text!r}")
    stock_text = await get_answer_by_key("stock") or "Пока нет текста 'stock'"
    try:
        print(f"Got stock_text from DB (or cache): {stock_text!r}")
        resp = await message.answer(stock_text, keyboard=back_menu_keyboard().get_json())
        print(f"Sent stock_text to user with back_menu_keyboard. Resp={resp}")
    except Exception as e:
        print(f"Error on message.answer: {e}")


@user_labeler.message(text=["Условия доставки", "Доставка"]) # get_locale("button.home_page.delivery")
async def handle_delivery(message: Message):
    delivery_text = await get_answer_by_key("delivery") or ""
    await message.answer(delivery_text, keyboard=back_menu_keyboard().get_json())


@user_labeler.message(text=["Подарки", "Заказать презенты(коробку,корзину,букет)"]) # get_locale("button.home_page.presents")
async def handle_presents(message: Message):
    presents_text = await get_answer_by_key("presents") or ""
    try:
        await message.answer(presents_text, keyboard=presents_keyboard().get_json())
    except Exception as e:
        print(f"Error on message.answer: {e}")

@user_labeler.message(text=["Десерты", "Десерты в шоколаде"]) # get_locale("button.home_page.desserts")
async def handle_desserts(message: Message):
    desserts_text = await get_answer_by_key("desserts") or ""
    await message.answer(desserts_text, keyboard=back_menu_keyboard().get_json())


@user_labeler.message(text=["Часы работы", "Время работы, адрес"]) # get_locale("button.home_page.working_hours")
async def handle_working_hours(message: Message):
    hours_text = await get_answer_by_key("working_hours") or ""
    await message.answer(hours_text, keyboard=back_menu_keyboard().get_json())


@user_labeler.message(text=["Отзывы", "Связаться с менеджером"]) # get_locale("button.home_page.feedback")
async def handle_feedback(message: Message):
    feedback_text = await get_answer_by_key("feedback") or ""
    await message.answer(feedback_text, keyboard=back_menu_keyboard().get_json())
