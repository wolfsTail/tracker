from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "google_id"
    YANDEX_TOKEN_ID: str = "yandex_id"
    DB_NAME: str = "local_db"
    DB_PASSWORD: str
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
