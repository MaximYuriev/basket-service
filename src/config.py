from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")


class PostgresConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RMQConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="RMQ_")
    host: str
    port: str
    user: str
    password: str

    @property
    def rmq_url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class Config(BaseSettings):
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    rmq: RMQConfig = Field(default_factory=RMQConfig)
