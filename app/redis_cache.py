import aioredis
from app.config import REDIS_URL, CACHE_TTL

redis = None

async def init_redis():
    """
    Инициализация глобального Redis клиента (асинхронно).
    Вызываем при старте приложения (например, в main.py).
    """
    global redis
    redis = await aioredis.from_url(
        REDIS_URL,
        encoding="utf-8",
        decode_responses=True  # чтобы автоматически декодировать строку в UTF-8
    )

async def get_from_cache(key: str):
    """
    Получить значение из кэша по ключу.
    Возвращает None, если ключа нет.
    """
    if redis is None:
        return None
    return await redis.get(key)

async def set_to_cache(key: str, value: str, ttl: int = None):
    """
    Сохранить в кэше значение по ключу на ttl (в минутах).
    Если ttl не указан, используем значение из конфига (CACHE_TTL).
    """
    if redis is None:
        return
    if ttl is None:
        ttl = CACHE_TTL
    # Redis ждет ttl в секундах
    ttl_in_seconds = ttl * 60
    await redis.set(key, value, ex=ttl_in_seconds)

async def delete_cache(key: str):
    """
    Удалить ключ из кэша.
    """
    if redis is None:
        return
    await redis.delete(key)
