from pydantic_settings import BaseSettings, SettingsConfigDict
from authx import AuthXConfig

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 900
    JWT_REFRESH_TOKEN_EXPIRES: int = 604800

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_TOKEN_EXPIRES = settings.JWT_ACCESS_TOKEN_EXPIRES
config.JWT_REFRESH_TOKEN_EXPIRES = settings.JWT_REFRESH_TOKEN_EXPIRES

config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_REFRESH_COOKIE_NAME = "refresh_token"
config.JWT_COOKIE_SECURE = True  # Тільки HTTPS
config.JWT_COOKIE_SAMESITE = "Lax"  # Захист від CSRF

config.JWT_COOKIE_CSRF_PROTECT = True
config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access"
config.JWT_REFRESH_CSRF_COOKIE_NAME = "csrf_refresh"

