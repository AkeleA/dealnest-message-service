from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./app.db")
    REDIS_URL: str = "rediss://default:ASVbAAImcDI5NzMyMDM0ZTAxYzE0YTJmOTU4YjE3YzU0ZDkwZmYxMnAyOTU2Mw@free-drake-9563.upstash.io:6379"
    DEFAULT_NOTIFICATION_DELAY_MINUTES: int = 1
    EMAIL_SENDER: str = "noreply@dealnest.test"
    CELERY_TASK_ALWAYS_EAGER: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
