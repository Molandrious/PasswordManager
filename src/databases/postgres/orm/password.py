from sqlalchemy.orm import Mapped, mapped_column

from src.databases.postgres.orm.base import BaseORM


class PasswordORM(BaseORM):
    service_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
