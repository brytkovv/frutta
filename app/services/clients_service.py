from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.client import Client
from app.redis_cache import get_from_cache, set_to_cache
from app.config import CACHE_TTL


CACHE_PREFIX = "clients_exists"

async def is_client_exists(vk_id: int) -> bool:
    """
    Возвращает True, если клиент с таким vk_id есть в БД,
    False - если нет.
    При этом используется кэш Redis (строка "1" или "0").
    """
    cache_key = f"{CACHE_PREFIX}:{vk_id}"
    cached = await get_from_cache(cache_key)
    if cached is not None:
        return cached == "1"

    # Если в кэше нет, проверяем БД
    async with SessionLocal() as session:
        stmt = select(Client).where(Client.vk_id == vk_id)
        result = await session.execute(stmt)
        client = result.scalar_one_or_none()
        exists = (client is not None)
        # Пишем в кэш "1" или "0"
        await set_to_cache(cache_key, "1" if exists else "0", CACHE_TTL)
        return exists


async def create_client(vk_id: int) -> Client:
    """
    Создаёт запись о клиенте (если нет). Возвращает модель Client.
    Если запись уже есть, возвращается существующая.
    После создания или выявления существующего клиента — кладёт "1" в кэш.
    """
    # Можно сначала проверить кэш (is_client_exists), но
    # при гонках (двойной запрос) на всякий случай отлавливаем IntegrityError в БД.
    async with SessionLocal() as session:
        new_client = Client(vk_id=vk_id)
        session.add(new_client)
        try:
            await session.commit()
        except IntegrityError:
            # Значит, запись уже существует
            await session.rollback()
            # Достаём и возвращаем
            async with SessionLocal() as session2:
                stmt = select(Client).where(Client.vk_id == vk_id)
                result = await session2.execute(stmt)
                existing_client = result.scalar_one()
                # Пропишем в кэш, что клиент точно есть
                cache_key = f"{CACHE_PREFIX}:{vk_id}"
                await set_to_cache(cache_key, "1", CACHE_TTL)
                return existing_client
        else:
            await session.refresh(new_client)

        # Успешно создан
        cache_key = f"{CACHE_PREFIX}:{vk_id}"
        await set_to_cache(cache_key, "1", CACHE_TTL)
        return new_client
