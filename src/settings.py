from enum import auto, StrEnum
from pathlib import Path

from pydantic import DirectoryPath, Field, PostgresDsn, RedisDsn, SecretBytes
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).parent.parent.resolve()

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#environment-variable-names


class Environment(StrEnum):
    @classmethod
    def _missing_(cls, value: str) -> str | None:
        value_lower = value.lower()
        for member in cls:
            if member.name.lower() == value_lower:
                return member
        return None

    TESTS = auto()
    LOCAL = auto()
    DEV = auto()
    PROD = auto()


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH.joinpath('.env'),
        extra='ignore',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
    )


class RESTSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REST_')

    host: str = Field(default='127.0.0.1')
    port: int = Field(default=8000)


class TestsSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TEST_')

    create_docker_postgres_for_tests: bool = Field(default=True)
    postgres_dsn: PostgresDsn | None = Field(
        default=PostgresDsn('postgresql+asyncpg://postgres:postgres@localhost:5432/testdb'),
    )


class PostgresSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    dsn: PostgresDsn
    echo: bool = Field(default=False)
    pool_size: int = Field(default=100)
    pool_timeout: int = Field(default=10)
    max_overflow: int = Field(default=10)
    pool_pre_ping: bool = Field(default=True)


class RedisSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_')

    dsn: RedisDsn = Field(default=RedisDsn('redis://localhost:6380/0'))


class EnvSettings(_BaseSettings):
    environment: Environment = Field(default=Environment.LOCAL)
    rest: RESTSettings = RESTSettings()
    tests: TestsSettings = TestsSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    secret_key: SecretBytes


class Settings(BaseSettings):
    env: EnvSettings = EnvSettings()

    root_path: DirectoryPath = Path(__file__).parent.parent.resolve()

    def __hash__(self):
        return hash(str(self.env.environment))


def get_settings() -> Settings:
    settings = Settings()

    # TODO: оставить тут или перенести в pytest_configure?
    if settings.env.environment == Environment.TESTS:
        if settings.env.tests.create_docker_postgres_for_tests:
            settings.env.postgres.dsn = PostgresDsn('postgresql+asyncpg://testuser:testpassword@localhost:5433/testdb')
        else:
            if not settings.env.tests.postgres_dsn:
                raise ValueError('TEST_POSTGRES_DSN environment variable is not set')
            settings.env.postgres.dsn = settings.env.tests.postgres_dsn

    return settings

