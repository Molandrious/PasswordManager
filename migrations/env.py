import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config
load_dotenv(config.get_main_option('env_file'), override=True)
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.databases.postgres.orm.base import BaseDeclarative
from src.settings import get_settings


if not (db:= config.get_main_option("sqlalchemy.url")):
    db = get_settings().env.postgres.dsn.unicode_string()

config.set_main_option('sqlalchemy.url', db.replace('postgresql+asyncpg', 'postgresql'))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseDeclarative.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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
