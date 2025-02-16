from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import DATABASE_URL


if DATABASE_URL.startswith("postgres://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    ASYNC_DATABASE_URL = DATABASE_URL

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # echo=True для отладки (вывод запросов)
    future=True
)

# Создаем базовую декларативную модель
Base = declarative_base()

# Фабрика сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


async def init_db():
    """
    Функция инициализации БД, например создание таблиц,
    если не используем Alembic, либо можно дернуть Alembic:
    >>> from alembic.config import Config
    >>> from alembic import command
    >>> alembic_cfg = Config("alembic.ini")
    >>> command.upgrade(alembic_cfg, "head")
    """
    async with engine.begin() as conn:
        # Если нужен create_all без Alembic (только для тестов или MVP)
        # await conn.run_sync(Base.metadata.create_all)

        # Либо здесь можно вызывать Alembic командами, если хочешь
        pass
