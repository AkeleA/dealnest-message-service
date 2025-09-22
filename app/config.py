from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./app.db")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    DEFAULT_NOTIFICATION_DELAY_MINUTES: int = 1
    EMAIL_SENDER: str = "noreply@dealnest.test"
    CELERY_TASK_ALWAYS_EAGER: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
