from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


class AsyncDBTransaction:
    def __init__(self, session: AsyncSession):
        self.session = session

    @asynccontextmanager
    async def use(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            yield self.session
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()


async def init_transaction(transaction: AsyncDBTransaction):
    async with transaction.use() as session:
        yield session
