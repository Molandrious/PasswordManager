from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, DirectoryPath, Field, PostgresDsn, SecretBytes
from pydantic_settings import BaseSettings, SettingsConfigDict

UpperStr = Annotated[str, AfterValidator(lambda v: v.upper())]
ROOT_PATH = Path(__file__).parent.parent.resolve()

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#environment-variable-names


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH.joinpath('.env'),
        extra='ignore',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
    )


class RESTSettings(_BaseSettings):
    host: str = Field(default='127.0.0.1')
    port: int = Field(default=8000)


class TestsSettings(_BaseSettings):
    create_docker_postgres_for_tests: bool = Field(default=True)
    local_test_db_dsn: PostgresDsn = Field(
        default=PostgresDsn('postgresql+asyncpg://postgres:postgres@localhost:5432/testdb'),
    )
    docker_test_db_dsn: PostgresDsn = Field(
        default=PostgresDsn('postgresql+asyncpg://testuser:testpassword@localhost:5433/testdb')
    )


class PostgresSettings(_BaseSettings):
    dsn: PostgresDsn
    echo: bool = Field(default=False)
    pool_size: int = Field(default=100)
    pool_timeout: int = Field(default=10)
    max_overflow: int = Field(default=10)
    pool_pre_ping: bool = Field(default=True)


class EnvSettings(_BaseSettings):
    rest: RESTSettings = RESTSettings(_env_prefix='REST_')  # type: ignore
    tests: TestsSettings = TestsSettings(_env_prefix='TEST_')  # type: ignore
    postgres: PostgresSettings = PostgresSettings(_env_prefix='POSTGRES_')  # type: ignore

    secret_key: SecretBytes


class Settings(BaseSettings):
    env: EnvSettings = EnvSettings()
    root_path: DirectoryPath = Path(__file__).parent.parent.resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
