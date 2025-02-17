from vkbottle import BaseStateGroup, BuiltinStateDispenser
from vkbottle.bot import BotLabeler, Message

from app.services.answers_service import get_all_can_change_answers, update_answer
from app.utils.keyboards import admin_keyboard, confirm_decline_keyboard, back_menu_keyboard
from app.localization import get_locale
from app.config import VK_ADMIN_IDS

admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True  # чтобы обрабатывало сообщения без учёта регистра

# ВАЖНО: Используем state_dispenser через message_view
sd = BuiltinStateDispenser()

class AdminState(BaseStateGroup):
    # В старых версиях BaseStateGroup значения должны быть целочисленными
    WAITING_FOR_KEY_CHOICE = 0
    WAITING_FOR_NEW_TEXT = 1
    CONFIRMING_NEW_TEXT = 2


async def show_admin_menu(message: Message):
    """Вспомогательная функция, чтобы показать меню админа"""
    answers = await get_all_can_change_answers()
    if not answers:
        await message.answer("Нет доступных для изменения записей.", keyboard=back_menu_keyboard().get_json())
        # state не выставляем, просто закончили логику
        return

    descriptions = [a.description or a.key for a in answers]
    await message.answer(
        "Выберите пункт для изменения:",
        keyboard=admin_keyboard(descriptions).get_json()
    )
    # Переходим в состояние "ждём, какой пункт выберет"
    await sd.set(message.peer_id, AdminState.WAITING_FOR_KEY_CHOICE)


@admin_labeler.message(state=AdminState.WAITING_FOR_KEY_CHOICE)
async def admin_choose_key(message: Message):
    """
    Пользователь-админ выбрал кнопку (description), нужно найти соответствующий Answer.
    """
    answers = await get_all_can_change_answers()
    chosen_answer = None
    for ans in answers:
        desc = ans.description or ans.key
        if desc == message.text:
            chosen_answer = ans
            break

    # Если не нашли, может это "назад"
    if not chosen_answer:
        if message.text.lower() == get_locale("button.back").lower():
            # Возвращаемся в главное меню
            from app.handlers.menu import back_to_menu
            await back_to_menu(message)
            # Сбросим состояние
            await sd.delete(message.peer_id)
            return

        await message.answer("Не понял, выберите из списка или нажмите 'Назад'.")
        return

    # Если нашли, просим новый текст
    await sd.set(
        peer_id=message.peer_id,
        state=AdminState.WAITING_FOR_NEW_TEXT,
        # в старых версиях state_dispenser.set(...) принимает дополнительный словарь во 2м параметре
        # но в 3.0.0 можно передавать keyword-аргументом: `chosen_key=...`
        chosen_key=chosen_answer.key
    )
    await message.answer("Введите новый текст (до 4096 символов):")


@admin_labeler.message(state=AdminState.WAITING_FOR_NEW_TEXT)
async def admin_input_new_text(message: Message):
    """ Сохраняем введённый текст во временные данные, спрашиваем подтверждение. """
    # Обновим data
    current_data = await sd.get(message.peer_id)
    chosen_key = current_data.payload.get("chosen_key")
    new_data = current_data.payload.copy()
    new_data["new_text"] = message.text

    # Переводим в состояние CONFIRMING_NEW_TEXT
    await sd.set(
        peer_id=message.peer_id,
        state=AdminState.CONFIRMING_NEW_TEXT,
        **new_data
    )
    await message.answer(
        f"Ваш новый текст:\n\n{message.text}\n\nПодтвердить?",
        keyboard=confirm_decline_keyboard().get_json()
    )


@admin_labeler.message(state=AdminState.CONFIRMING_NEW_TEXT)
async def admin_confirm_new_text(message: Message):
    """ Ждём "подтвердить" или "отменить". """
    current_data = await sd.get(message.peer_id)
    chosen_key = current_data.payload.get("chosen_key")
    new_text = current_data.payload.get("new_text")

    user_input = message.text.lower()
    if user_input == get_locale("text.confirm").lower():
        # Обновляем БД
        await update_answer(chosen_key, new_text)
        await message.answer(f"Обновлено.\nKey: {chosen_key}\n\nНовый текст:\n{new_text}")
        # Снова показываем меню админа (но состояние сбрасывать не обязательно; можно заново показать)
        await show_admin_menu(message)

    elif user_input == get_locale("text.decline").lower():
        await message.answer("Отменено.")
        # Снова показываем меню админа
        await show_admin_menu(message)
    else:
        await message.answer("Нужно выбрать Подтвердить или Отменить.")
        return


@admin_labeler.message(text=["Админка", get_locale("button.admin")])
async def admin_menu(message: Message):
    """ Вход в админку (не в FSM) """
    if message.from_id not in VK_ADMIN_IDS:
        await message.answer("Нет доступа.")
        return
    await show_admin_menu(message)
