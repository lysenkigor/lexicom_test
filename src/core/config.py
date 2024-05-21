from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    redis_host: str = Field(default=...)
    redis_port: int = Field(default=...)
    redis_db: int = 1

    @property
    def redis_url(self):
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}?decode_responses=True'


settings = Settings()
