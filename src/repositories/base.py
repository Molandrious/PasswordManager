from abc import ABC
from typing import Any, cast
from uuid import UUID

from sqlalchemy import or_, select, Select
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.databases.postgres.constants import UNIQUE_VIOLATION_ERROR_CODE
from src.databases.postgres.orm.base import BaseORM
from src.errors import ObjectAlreadyExistsError
from src.models.base import BaseEntity


class ISqlAlchemyRepository[ORM: BaseORM, Entity: BaseEntity](ABC):
    _model: ORM
    _session: AsyncSession
    _entity: Entity
    _model_search_fields: list[InstrumentedAttribute[Any]] | None = None

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_search(
        self,
        *,
        query: Select[tuple[ORM]],
        search: str | None = None,
    ) -> Select[tuple[ORM]]:
        if search is not None and self._model_search_fields:
            search = f'%{search}%'
            clauses = []
            models = set()
            for search_field in self._model_search_fields:
                search_field_model = search_field.parent.class_
                if search_field_model != self._model:
                    models.add(search_field_model)
                clauses.append(search_field.ilike(search))

            query = query.filter(or_(*clauses))
            for model in models:
                query = query.join(model)
        return query

    async def create(self, db_object: ORM) -> UUID:
        self._session.add(db_object)

        try:
            await self._session.flush()
        except IntegrityError as ex:
            if (
                isinstance(ex.orig, AsyncAdapt_asyncpg_dbapi.IntegrityError)
                and ex.orig.pgcode == UNIQUE_VIOLATION_ERROR_CODE
            ):
                raise ObjectAlreadyExistsError from ex

            raise

        await self._session.refresh(db_object)
        return cast(UUID, db_object.id)

    async def get_one_by(self, **kwargs) -> Entity | None:
        query = select(self._model).filter_by(**kwargs).limit(1)
        db_object = await self._session.scalar(query)
        return self._entity.model_validate(db_object) if db_object else None

    async def get_list(
        self,
        ids: list[UUID] | None = None,
        search: str | None = None,
        *,
        with_lock: bool = False,
        **filters: Any,
    ) -> list[ORM]:
        query = select(self._model)

        query = self._apply_search(query=query, search=search)

        if ids:
            query = query.where(self._model.id.in_(ids))

        if filters:
            query = query.filter_by(**filters)

        if with_lock:
            query = query.with_for_update()

        db_objects = await self._session.scalars(query)
        return list(db_objects.all())

    async def update_object(self, db_object: ORM) -> None:
        await self._session.merge(db_object)


