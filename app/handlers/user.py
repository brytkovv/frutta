from vkbottle.bot import Blueprint, Message
from app.services.answers_service import get_answer_by_key
from app.utils.keyboards import back_menu_keyboard, presents_keyboard
from app.localization import get_locale
from app.config import GROUP_ID, MANAGER_PHONE, MANAGER_ID

user_bp = Blueprint(name="user_blueprint")

@user_bp.on.message(text="Акции")  # match c локалью button.home_page.stock
async def handle_stock(message: Message):
    # Достаем контент из БД/кэша
    stock_text = await get_answer_by_key("stock") or "Пока нет текста 'stock'"
    await message.answer(stock_text, keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Доставка")
async def handle_delivery(message: Message):
    delivery_text = await get_answer_by_key("delivery") or "Текст не найден"
    await message.answer(delivery_text, keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Подарки")  # presents
async def handle_presents(message: Message):
    presents_text = await get_answer_by_key("presents") or ""
    # Здесь есть своё меню
    await message.answer(presents_text, keyboard=presents_keyboard().get_json())

@user_bp.on.message(text="Десерты")
async def handle_desserts(message: Message):
    desserts_text = await get_answer_by_key("desserts") or ""
    await message.answer(desserts_text, keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Часы работы")
async def handle_working_hours(message: Message):
    hours_text = await get_answer_by_key("working_hours") or ""
    await message.answer(hours_text, keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Отзывы")
async def handle_feedback(message: Message):
    feedback_text = await get_answer_by_key("feedback") or ""
    await message.answer(feedback_text, keyboard=back_menu_keyboard().get_json())


# --- Подменю "presents" ---
@user_bp.on.message(text="Каталог")
async def handle_catalog(message: Message):
    # Ссылка на товары (market) группы: https://vk.com/market-GROUP_ID
    catalog_url = f"https://vk.com/market-{GROUP_ID}"
    # ВКонтакте может не поддерживать «кликабельный» текст,
    # можно отправить как ссылка, либо кнопка-ссылка (inline).
    text_reply = f"Перейдите в наш каталог: {catalog_url}"
    await message.answer(text_reply, keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Позвонить")
async def handle_call(message: Message):
    # Часто делают ссылку "tel:MANAGER_PHONE"
    phone_link = f"tel:{MANAGER_PHONE}"
    await message.answer(f"Набираем номер: {phone_link}", keyboard=back_menu_keyboard().get_json())

@user_bp.on.message(text="Написать менеджеру")
async def handle_direct_message(message: Message):
    # Ссылка на чат: https://vk.com/im?sel=MANAGER_ID
    dm_link = f"https://vk.com/im?sel={MANAGER_ID}"
    direct_text = get_locale("text.direct_message")
    full_text = f"{direct_text}\nСсылка для чата: {dm_link}"
    await message.answer(full_text, keyboard=back_menu_keyboard().get_json())
