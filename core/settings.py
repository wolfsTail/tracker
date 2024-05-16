from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str = "google_id"
    GOOGLE_REDIRECT_URI: str = "GOOLE_URI"
    GOOGLE_TOKEN_URL: str = "https://accounts_google.com/o/oauth2/token"
    GOOGLE_CLIENT_SECRET: str = "google_secret"
    YANDEX_TOKEN_ID: str = "yandex_id"
    DB_USER: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "local_db"
    DB_PASSWORD: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str
    REDIS_DB: str

    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "secret"

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    @property
    def GOOGLE_REDIRECT_URL(self):
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
  

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
