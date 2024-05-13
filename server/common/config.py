from pydantic_settings import BaseSettings, SettingsConfigDict

from common.constants import PROD

class Settings(BaseSettings):
    app_name: str = "PyKudos"
    admin_email: str
    secret_key: str
    algorithm: str
    token_expiration_in_minutes: int
    environment: str = PROD

    model_config = SettingsConfigDict(env_file=".env")