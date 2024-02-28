import os


class Config:
    APP_HOST: str = os.getenv("APP_HOST", default="0.0.0.0")  # Хост сервиса
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", default="")  # Пользователь бд PGSQL
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", default="")  # Пароль от бд PGSQL
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", default="")  # Название таблицы PGSQL
    REQUESTS_PER_MINUTE_LIMIT: int = int(os.getenv("REQUESTS_PER_MINUTE_LIMIT", default="600"))  # Лимит запросов в минуту
    DB_LOGS: bool = bool(os.getenv("DB_LOGS", default=False))  # Вкл\выкл логи sqlalchemy


config = Config()
