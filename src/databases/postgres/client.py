import contextlib

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.databases.postgres.orm.base import BaseDeclarative
from src.databases.postgres.uow import AsyncDBTransaction
from src.settings import PostgresSettings


class SQLAlchemyClient:
    def __init__(self, settings: PostgresSettings | dict) -> None:
        if isinstance(settings, dict):
            settings = PostgresSettings.model_validate(settings)

        self.engine = create_async_engine(
            url=settings.dsn.unicode_string(),
            echo=settings.echo,
            pool_size=settings.pool_size,
            pool_timeout=settings.pool_timeout,
            max_overflow=settings.max_overflow,
            pool_pre_ping=settings.pool_pre_ping,
        )
        self._session_factory = async_sessionmaker(expire_on_commit=False, bind=self.engine)

    @property
    def session(self) -> AsyncSession:
        return self._session_factory()

    @property
    def uow(self) -> AsyncDBTransaction:
        return AsyncDBTransaction(session=self.session)

    async def clear_all_tables(self) -> None:
        metadata = BaseDeclarative.metadata
        async with self.session as session:
            for table in reversed(metadata.sorted_tables):
                with contextlib.suppress(DatabaseError):
                    await session.execute(table.delete())
            await session.commit()

    async def create_all_tables(self) -> None:
        metadata = BaseDeclarative.metadata
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
