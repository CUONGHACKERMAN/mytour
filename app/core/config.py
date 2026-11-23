from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE: int = 60
    JWT_REFRESH_TOKEN_EXPIRE: int = 7
    CORS_ORIGINS: list[str]

    MEDIA_PROVIDER: str = "local"
    MEDIA_ROOT: str = "./storage/media"
    R2_API_KEY: str | None = None
    S3_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
