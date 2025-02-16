from vkbottle import Keyboard, Text
from app.localization import get_locale

def main_menu_keyboard():
    """
    Главное меню (stock, delivery, presents, desserts, working_hours, feedback).
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("button.home_page.stock")), color="primary")
    kb.add(Text(get_locale("button.home_page.delivery")), color="primary")
    kb.row()
    kb.add(Text(get_locale("button.home_page.presents")), color="primary")
    kb.add(Text(get_locale("button.home_page.desserts")), color="primary")
    kb.row()
    kb.add(Text(get_locale("button.home_page.working_hours")), color="primary")
    kb.add(Text(get_locale("button.home_page.feedback")), color="primary")

    return kb

def presents_keyboard():
    """
    Подменю "presents" (catalog, call, direct_message) + «назад».
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("button.presents.catalog")), color="primary")
    kb.add(Text(get_locale("button.presents.call")), color="primary")
    kb.row()
    kb.add(Text(get_locale("button.presents.direct_message")), color="secondary")
    kb.row()
    kb.add(Text(get_locale("button.back")), color="negative")  # "назад"
    return kb

def back_menu_keyboard():
    """
    Одна кнопка "назад". Можно использовать в любом месте, где нам нужно вернуться в главное меню.
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("button.back")), color="negative")
    return kb

def admin_keyboard(descriptions):
    """
    Клавиатура для админа: список кнопок (по их description) + назад.
    descriptions: список строк, каждая — description записи, которую можно изменить.
    """
    kb = Keyboard(inline=False)
    for desc in descriptions:
        kb.add(Text(desc), color="primary")
        kb.row()
    kb.add(Text(get_locale("button.back")), color="negative")
    return kb

def confirm_decline_keyboard():
    """
    Кнопки подтверждения/отмены изменения.
    """
    kb = Keyboard(inline=False)
    kb.add(Text(get_locale("text.confirm")), color="positive")
    kb.add(Text(get_locale("text.decline")), color="negative")
    return kb
