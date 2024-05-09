from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "google_id"
    YANDEX_TOKEN_ID: str = "yandex_id"
    DB_USER: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = 5432
    DB_NAME: str = "local_db"
    DB_PASSWORD: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str
    REDIS_DB: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:
        {self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
