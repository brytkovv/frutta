from vkbottle import Keyboard, Text, OpenLink, KeyboardButtonColor
from app.localization import get_locale
from app.config import GROUP_ID, MANAGER_PHONE, MANAGER_ID

def main_menu_keyboard():
    """
    Главное меню (stock, delivery, presents, desserts, working_hours, feedback).
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("button.home_page.stock")))
    kb.row()
    kb.add(Text(get_locale("button.home_page.presents")))
    kb.row()
    kb.add(Text(get_locale("button.home_page.delivery")), color=KeyboardButtonColor.NEGATIVE)
    kb.add(Text(get_locale("button.home_page.desserts")), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text(get_locale("button.home_page.working_hours")), color=KeyboardButtonColor.PRIMARY)
    kb.row()

    kb.add(Text(get_locale("button.home_page.feedback")), color=KeyboardButtonColor.SECONDARY)

    return kb

def presents_keyboard():
    """
    Подменю "presents" (catalog, call, direct_message) + «назад».
    """
    kb = Keyboard(inline=False)
    kb.add(OpenLink(
        label=get_locale("button.presents.catalog"),
        link=f"https://vk.com/market-{GROUP_ID}"
    ))
    kb.row()
    kb.add(OpenLink(
        label=get_locale("button.presents.call"),
        link=f"tel:+{MANAGER_PHONE}"
    ))
    kb.row()
    # TODO: без текста ((((
    kb.add(OpenLink(
        label=get_locale("button.presents.direct_message"),
        link=f"https://vk.com/im?sel={MANAGER_ID}" # {get_locale('button.text.direct_message')}
    ))
    kb.row()
    kb.add(Text(get_locale("button.back")))  # "назад"
    return kb

def back_menu_keyboard():
    """
    Одна кнопка "назад". Можно использовать в любом месте, где нам нужно вернуться в главное меню.
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("button.back")))
    return kb

def admin_keyboard(descriptions):
    """
    Клавиатура для админа: список кнопок (по их description) + назад.
    descriptions: список строк, каждая — description записи, которую можно изменить.
    """
    kb = Keyboard(inline=False)
    for desc in descriptions:
        kb.add(Text(desc))
        kb.row()
    kb.add(Text(get_locale("button.back")))
    return kb

def confirm_decline_keyboard():
    """
    Кнопки подтверждения/отмены изменения.
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("text.confirm")))
    kb.add(Text(get_locale("text.decline")))
    return kb
