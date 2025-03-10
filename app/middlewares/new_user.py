from typing import List, Any

from vkbottle import BaseMiddleware
from vkbottle.bot import Message
from vkbottle.dispatch.views.abc import ABCView
from vkbottle.dispatch.handlers.abc import ABCHandler

from app.services.clients_service import is_client_exists, create_client
from app.utils.keyboards import main_menu_keyboard
from app.localization import get_locale
from app.utils.logs import logger
from app.services.answers_service import get_answer_by_key


class NewUserMiddleware(BaseMiddleware):
    """
    Мидлварь, которая:
      1) Проверяет, есть ли пользователь в БД (pre).
      2) Если пользователя нет — создаёт его (фиксируем флаг self.was_new_user).
      3) После обработки всеми хендлерами (post) смотрим, был ли он новым
         и не обработал ли его сообщение хотя бы один хендлер (handle_responses).
      4) Если реально новый и ни один хендлер не ответил — отправляем "Начать".
    """

    async def pre(self, event: Message, *args) -> bool:
        """
        Вызывается ДО хендлеров.
        Возвращаем True, чтобы пропустить событие дальше (в хендлеры).
        """
        self.was_new_user = False

        user_exists = await is_client_exists(event.from_id)
        if not user_exists:
            new_client = await create_client(event.from_id)
            self.was_new_user = True
            logger.info(
                f"[NewUserMiddleware] Создан новый клиент: id={new_client.id}, vk_id={event.from_id}"
            )

        return True

    async def post(
            self,
            event: Message,
            view: ABCView,
            handle_responses: List[Any],
            handlers: List[ABCHandler]
    ) -> bool:
        """
        Вызывается ПОСЛЕ хендлеров.
          - handle_responses: список результатов, которые вернули сработавшие хендлеры (пустой, если никто не сработал).
          - handlers: список хендлеров, которые потенциально могли обработать событие.

        Если пользователь новый (was_new_user = True) и ни один хендлер не вернул ответ,
        шлём "стартовый" текст и кнопку "Начать".
        """
        if self.was_new_user and not handle_responses:
            greetings = await get_answer_by_key("greeting") or ""
            await event.answer(greetings, keyboard=main_menu_keyboard().get_json())
            logger.info(f"[NewUserMiddleware] Отправлено 'menu' пользователю {event.from_id}")

        return True
