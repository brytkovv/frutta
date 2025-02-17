import yaml
import os

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "locales")
DEFAULT_LOCALE_FILE = os.path.join(LOCALES_DIR, "ru.yml")

_locale_dict = {}

def load_locale(file_path: str = DEFAULT_LOCALE_FILE) -> None:
    """
    Загружаем YAML-файл локализации в словарь _locale_dict.
    """
    global _locale_dict
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        _locale_dict = data.get("ru", {})  # берем вложенный ключ ru

def get_locale(path: str) -> str:
    """
    Получить строку из локали по пути вида: "text.greetings" или "button.home_page.stock"
    Если чего-то нет, вернем пустую строку (или можно выбросить ошибку).
    """
    # Разбиваем path на цепочку ключей
    keys = path.split(".")
    current = _locale_dict
    for k in keys:
        if k in current:
            current = current[k]
        else:
            return ""  # или None
    # current должен быть строкой, если всё ОК
    if isinstance(current, str):
        return current
    return ""
