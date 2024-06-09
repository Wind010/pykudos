from pydantic_settings import BaseSettings, SettingsConfigDict

from common.constants import PROD

class Settings(BaseSettings):
    app_name: str = "PyKudos"
    admin_email: str
    host_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_type: str
    database_connection_string: str
    environment: str = PROD
    allowed_hosts: list
    allowed_origins: list
    server_side_render: bool
    github_url: str
    github_pat: str
    github_orgs: list
    github_teams: list
    enable_local_auth: bool
    enable_github_auth: bool
    github_client_id: str
    github_client_secret: str


    model_config = SettingsConfigDict(env_file=".env")