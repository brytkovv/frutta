from vkbottle import BaseStateGroup
from vkbottle.bot import Blueprint, Message
from app.services.answers_service import get_all_can_change_answers, update_answer
from app.utils.keyboards import admin_keyboard, confirm_decline_keyboard, back_menu_keyboard
from app.localization import get_locale
from app.config import VK_ADMIN_IDS

admin_bp = Blueprint(name="admin_blueprint")

class AdminState(BaseStateGroup):
    WAITING_FOR_KEY_CHOICE = "waiting_for_key_choice"
    WAITING_FOR_NEW_TEXT = "waiting_for_new_text"
    CONFIRMING_NEW_TEXT = "confirming_new_text"


# Вспомогательная функция, чтобы показать меню админа
async def show_admin_menu(message: Message):
    answers = await get_all_can_change_answers()
    if not answers:
        await message.answer("Нет доступных для изменения записей.", keyboard=back_menu_keyboard().get_json())
        return

    # Соберём descriptions
    descriptions = [a.description or a.key for a in answers]
    await message.answer(
        "Выберите пункт для изменения:",
        keyboard=admin_keyboard(descriptions).get_json()
    )
    # Превращаем это в состояние "ждём, какой пункт выберет"
    await admin_bp.state_dispenser.set(message.peer_id, AdminState.WAITING_FOR_KEY_CHOICE)


@admin_bp.on.message(state=AdminState.WAITING_FOR_KEY_CHOICE)
async def admin_choose_key(message: Message):
    """
    Пользователь-админ выбрал кнопку (description), нужно найти соответствующий Answer.
    """
    # Попробуем найти соответствующий key
    answers = await get_all_can_change_answers()
    # Сопоставляем description => key
    chosen_answer = None
    for ans in answers:
        desc = ans.description or ans.key
        if desc == message.text:
            chosen_answer = ans
            break

    if not chosen_answer:
        # Если не нашли, может это "назад" или просто невалидный ввод?
        if message.text.lower() == get_locale("button.back").lower():
            # Возвращаемся в главное меню
            # Можно вызывать хендлер из menu_bp или просто отправить приветствие
            # и показать main_menu_keyboard
            from app.handlers.menu import back_to_menu
            await back_to_menu(message)
            # Сбрасываем стейт
            await admin_bp.state_dispenser.delete(message.peer_id)
            return

        await message.answer("Не понял, выберите из списка или нажмите 'Назад'.")
        return

    # Если нашли, просим ввести новый текст
    # Запишем key во временные данные FSM
    await admin_bp.state_dispenser.set(message.peer_id, AdminState.WAITING_FOR_NEW_TEXT, chosen_key=chosen_answer.key)
    await message.answer("Введите новый текст (до 4096 символов):")


@admin_bp.on.message(state=AdminState.WAITING_FOR_NEW_TEXT)
async def admin_input_new_text(message: Message):
    """
    Сохраняем введённый текст во временные данные, спрашиваем подтверждение.
    """
    # Сохраним новый текст
    await admin_bp.state_dispenser.update(message.peer_id, {"new_text": message.text})
    # Переходим в подтверждение
    await admin_bp.state_dispenser.set(message.peer_id, AdminState.CONFIRMING_NEW_TEXT)
    await message.answer(
        f"Ваш новый текст:\n\n{message.text}\n\nПодтвердить?",
        keyboard=confirm_decline_keyboard().get_json()
    )

@admin_bp.on.message(state=AdminState.CONFIRMING_NEW_TEXT)
async def admin_confirm_new_text(message: Message):
    """
    Ждём "подтвердить" или "отменить".
    """
    state_data = await admin_bp.state_dispenser.get(message.peer_id)
    chosen_key = state_data.payload["chosen_key"]
    new_text = state_data.payload["new_text"]

    # Смотрим, что нажал админ
    user_input = message.text.lower()
    if user_input == get_locale("text.confirm").lower():
        # Обновляем БД
        await update_answer(chosen_key, new_text)
        await message.answer(f"Обновлено.\nKey: {chosen_key}\n\nНовый текст:\n{new_text}")
        # Возвращаемся в админ-меню или главное меню
        await show_admin_menu(message)
    elif user_input == get_locale("text.decline").lower():
        await message.answer("Отменено.")
        # Возвращаемся в админ-меню
        await show_admin_menu(message)
    else:
        await message.answer("Нужно выбрать Подтвердить или Отменить.")
        return


# Если пользователь вне FSM ввел "Админка" (см. menu.py) → show_admin_menu(...)
@admin_bp.on.message(text="Админка")
async def admin_menu(message: Message):
    if message.from_id not in VK_ADMIN_IDS:
        await message.answer("Нет доступа.")
        return
    await show_admin_menu(message)
