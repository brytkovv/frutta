from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models.client import Client

async def get_client_by_vk_id(vk_id: int) -> Client | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Client).where(Client.vk_id == vk_id)
        )
        return result.scalar_one_or_none()

async def create_client(vk_id: int) -> Client:
    async with SessionLocal() as session:
        new_client = Client(vk_id=vk_id)
        session.add(new_client)
        try:
            await session.commit()
        except IntegrityError:
            # На случай гонки, если 2 раза подряд пришло сообщение от одного vk_id
            await session.rollback()
            return await get_client_by_vk_id(vk_id)
        await session.refresh(new_client)
        return new_client
