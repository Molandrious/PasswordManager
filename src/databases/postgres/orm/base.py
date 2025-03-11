from __future__ import annotations

from datetime import date, datetime
from typing import Any, ClassVar
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from pydantic.alias_generators import to_snake
from sqlalchemy import Date as SQLAlchemyDate, DateTime as SQLAlchemyDateTime, MetaData
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from src.databases.postgres.constants import CONSTRAINT_NAMING_CONVENTIONS


class BaseDeclarative(DeclarativeBase):
    metadata = MetaData(naming_convention=CONSTRAINT_NAMING_CONVENTIONS)

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        datetime: SQLAlchemyDateTime(timezone=True),
        date: SQLAlchemyDate,
        dict: JSONB,
    }


class BaseORM(BaseDeclarative):
    __abstract__ = True

    @classmethod
    @declared_attr.directive
    def __tablename__(cls):
        return to_snake(cls.__name__.rstrip("ORM"))

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
        default=uuid4,
        sort_order=-3,
    )

    created_at: Mapped[datetime] = mapped_column(
        insert_default=lambda: datetime.now(tz=ZoneInfo("Europe/Moscow")),
        nullable=False,
        sort_order=-2,
    )

    updated_at: Mapped[datetime] = mapped_column(
        insert_default=lambda: datetime.now(tz=ZoneInfo("Europe/Moscow")),
        onupdate=lambda: datetime.now(tz=ZoneInfo("Europe/Moscow")),
        nullable=True,
        sort_order=-1,
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} | {self.__dict__}>"
