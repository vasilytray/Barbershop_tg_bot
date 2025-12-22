import os
from typing import List

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    
    # Основная БД приложения
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    # DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'
    # STORE_URL: str = 'sqlite:///data/jobs.sqlite'
    
    # Сайты
    BASE_SITE: str
    TG_API_SITE: str
    FRONT_SITE: str
    
    # Настройки для хранилища задач планировщика
    SCHEDULER_DB_HOST: str 
    SCHEDULER_DB_PORT: int 
    SCHEDULER_DB_NAME: str
    SCHEDULER_DB_USER: str
    SCHEDULER_DB_PASSWORD: str
    
    # Настройки планировщика
    JOBSTORE_URL: str
    SCHEDULER_POOL_SIZE: int = 10
    SCHEDULER_MAX_INSTANCES: int = 3

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        env_file_encoding='utf-8',
        case_sensitive=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Автоматически создаем URL для планировщика
        if self.JOBSTORE_URL is None:
            self.JOBSTORE_URL = self.get_scheduler_db_url()
            
    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука."""
        return f"{self.BASE_SITE}/webhook"

    def get_tg_api_url(self) -> str:
        """Возвращает URL Telegram API."""
        return f"{self.TG_API_SITE}/bot{self.BOT_TOKEN}"
    
    def get_db_url(self):
        """Возвращает URL основной базы данных."""
        return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
                f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
        
    def get_scheduler_db_url(self) -> str:
        """Возвращает URL базы данных для планировщика."""
        return (f"postgresql://{self.SCHEDULER_DB_USER}:{self.SCHEDULER_DB_PASSWORD}@"
                f"{self.SCHEDULER_DB_HOST}:{self.SCHEDULER_DB_PORT}/{self.SCHEDULER_DB_NAME}")

# Инициализация настроек и планировщика задач
settings = Settings() # type: ignore

# Инициализация планировщика с PostgreSQL хранилищем
scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(
            url=settings.JOBSTORE_URL,
            engine_options={
                'pool_size': settings.SCHEDULER_POOL_SIZE,
                'max_overflow': 5,
                'pool_timeout': 30,
                'pool_recycle': 3600,
            }
        )
    },
    job_defaults={
        'coalesce': True,  # объединять пропущенные задачи
        'max_instances': settings.SCHEDULER_MAX_INSTANCES,
        'misfire_grace_time': 30  # секунд
    },
    timezone='UTC'
)