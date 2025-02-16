from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.redis_cache import get_from_cache, set_to_cache, delete_cache
from app.database import SessionLocal
from app.models.answer import Answer
from app.config import CACHE_TTL


async def get_answer_by_key(key: str) -> Optional[str]:
    """
    Достаём message по key из кэша Redis или (при отсутствии) из БД.
    """
    cache_key = f"answers:{key}"
    cached = await get_from_cache(cache_key)
    if cached is not None:
        return cached

    # Если нет в кэше — берём из БД
    async with SessionLocal() as session:
        stmt = select(Answer).where(Answer.key == key)
        result = await session.execute(stmt)
        answer_obj = result.scalar_one_or_none()
        if answer_obj:
            # Кладём в кэш
            await set_to_cache(cache_key, answer_obj.message or "", CACHE_TTL)
            return answer_obj.message
        else:
            # Нет такого key в БД
            return None

async def update_answer(key: str, new_message: str) -> bool:
    """
    Обновляет message в БД, удаляет из кэша.
    Возвращает True, если запись найдена и обновлена, иначе False.
    """
    async with SessionLocal() as session:
        stmt = select(Answer).where(Answer.key == key)
        result = await session.execute(stmt)
        answer_obj = result.scalar_one_or_none()

        if not answer_obj:
            return False

        answer_obj.message = new_message
        session.add(answer_obj)
        await session.commit()

    # Удаляем из кэша
    cache_key = f"answers:{key}"
    await delete_cache(cache_key)
    return True


async def get_all_can_change_answers() -> List[Answer]:
    """
    Возвращает список записей answers, у которых can_change = True.
    """
    async with SessionLocal() as session:
        stmt = select(Answer).where(Answer.can_change == True)
        result = await session.execute(stmt)
        return result.scalars().all()
