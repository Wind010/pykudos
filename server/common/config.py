from pydantic_settings import BaseSettings, SettingsConfigDict

from common.constants import PROD

class Settings(BaseSettings):
    app_name: str = "PyKudos"
    admin_email: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_type: str
    database_connection_string: str
    environment: str = PROD
    allowed_hosts: list

    model_config = SettingsConfigDict(env_file=".env")