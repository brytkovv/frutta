# app/middleware/new_user.py
import logging
from typing import Union
from vkbottle import BaseMiddleware, MiddlewareResponse
from vkbottle.bot import Message

from app.services.clients_service import get_client_by_vk_id, create_client
from app.utils.keyboards import start_keyboard
from app.localization import get_locale


class NewUserMiddleware(BaseMiddleware[Message]):
    """
    Мидлварь, которая:
      1) Проверяет, есть ли пользователь в БД (pre).
      2) Если пользователя нет - создаёт его, фиксируя флаг "was_new_user".
      3) После обработки всеми хендлерами (post) смотрит, был ли он новым и
         никто ли не обработал сообщение (handler_return is None).
      4) Если реально новый и никто не ответил - отправляет "Начать".
    """

    async def pre(self) -> Union[bool, MiddlewareResponse]:
        """Срабатывает ДО хендлеров."""
        message: Message = self.event
        self.was_new_user = False  # флаг, чтобы пост знать, что мы кого-то добавили

        user_in_db = await get_client_by_vk_id(message.from_id)
        if not user_in_db:
            # Создаём запись
            new_client = await create_client(message.from_id)
            self.was_new_user = True
            logging.info(f"[NewUserMiddleware] Создан новый клиент id={new_client.id}, vk_id={message.from_id}")

        # Возвращаем True, чтобы остальные хендлеры смогли обработать сообщение
        return True

    async def post(self) -> Union[bool, MiddlewareResponse]:
        """Срабатывает ПОСЛЕ хендлеров."""
        # self.handler_return — что вернул хендлер (или None, если ни один не сработал)
        # self.was_new_user — наш флаг из pre()
        if self.was_new_user and self.handler_return is None:
            # Пользователь новый, и никто из хендлеров не взял на себя это сообщение
            start_text = get_locale("text.start")
            kb = start_keyboard()  # Кнопка "Начать"
            await self.event.answer(start_text, keyboard=kb.get_json())
            # Можно логировать, что мы выслали "fallback" для нового пользователя
            logging.info(f"[NewUserMiddleware] Отправлено 'start' пользователю {self.event.from_id}")

        return True
