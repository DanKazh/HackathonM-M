from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Вычисляем путь к корню проекта
# Текущий файл: backend/app/repo/alembic/env.py
# Поднимаемся на 4 уровня вверх до корня проекта
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent.parent.parent

# Добавляем корень проекта в Python path
sys.path.insert(0, str(project_root))

# Загружаем переменные окружения из .env файла в корне проекта
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"Loaded .env from: {env_path}")
else:
    print(f".env file not found at: {env_path}")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Переопределяем URL базы данных из переменных окружения
database_url = os.getenv('DATABASE_URL')
if not database_url:
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_name = os.getenv('POSTGRES_DB', 'astronomy_db')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASS', 'password')
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

if database_url:
    config.set_main_option('sqlalchemy.url', database_url)
    print("Using database URL from .env")
else:
    print("No database configuration found")
    # Используем fallback URL для предотвращения ошибки
    fallback_url = 'postgresql://postgres:password@localhost:5432/astronomy_db'
    config.set_main_option('sqlalchemy.url', fallback_url)
    print(f"Using fallback URL: {fallback_url}")

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()