from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAuthorizerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")


class CookieConfig(BaseAuthorizerConfig):
    model_config = SettingsConfigDict(env_prefix="COOKIE_")
    name: str


class SSLConfig(BaseAuthorizerConfig):
    model_config = SettingsConfigDict(env_prefix="SSL_")
    private_key_path: Path
    public_key_path: Path


class AuthorizerConfig(BaseSettings):
    cookie: CookieConfig = Field(default_factory=CookieConfig)
    ssl: SSLConfig = Field(default_factory=SSLConfig)

authorizer_config = AuthorizerConfig()
