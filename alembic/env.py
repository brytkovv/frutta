import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()

from app.database import Base

# Это Alembic Config объект, который читает настройки из alembic.ini
config = context.config

# Устанавливаем логирование из файла alembic.ini
fileConfig(config.config_file_name)

# Метаданные, с которыми Alembic будет сравнивать состояние БД
target_metadata = Base.metadata

# -------------------------------------------------------------------------
# Переопределяем sqlalchemy.url из ENV (если нужно)
# -------------------------------------------------------------------------
# Можно считать ENV напрямую

if os.getenv("DATABASE_URL").startswith("postgres://"):
    DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "")

config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """
    Запуск миграций в режиме "offline".
    В этом режиме Alembic не подключается к БД,
    а формирует SQL-скрипты на основе настроек.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # compare_type=True, если нужно сравнивать типы полей
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Запуск миграций в режиме "online".
    Фактически Alembic коннектится к реальной БД и прогоняет миграции.
    """
    # Создаём движок на основе config (из alembic.ini + env override)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # future=True  # можно указать, если хотите режим future SQLAlchemy
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # compare_type=True  # если надо проверять изменения типов
        )

        with context.begin_transaction():
            context.run_migrations()


# Alembic сам решит, какой режим запустить (offline/online),
# смотря на параметры в alembic.ini или ключи, переданные в CLI
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
