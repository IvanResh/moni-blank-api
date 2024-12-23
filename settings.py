import pathlib

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

current_directory = pathlib.Path(__file__).parent.resolve()
env_path = pathlib.Path(current_directory, ".env")


class Settings(BaseSettings):
    """Settings class for src."""

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    testing: bool = False
    debug: bool = False

    web_port: int = 8000
    web_app_url: str = "http://localhost:8000"

    sentry_dsn: str | None = None
    environment: str = "local"

    db_host: str = "127.0.0.1"
    db_port: int = 5433
    db_user: str = "postgres"
    db_password: SecretStr = "postgres"  # type: ignore
    db_name: str = "postgres"
    db_pool_min_size: int = 1
    db_pool_max_size: int = 50
    db_command_timeout: int = 10

    @property
    def db_dsn(self) -> str:
        if self.testing:
            db_name = self.test_db_name
        else:
            db_name = self.db_name
        return f"postgresql://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{db_name}"

    @property
    def test_db_name(self) -> str:
        return "test_" + self.db_name


def get_settings() -> Settings:
    settings = Settings()
    return settings
