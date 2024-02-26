import os


class Config:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", default="")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", default="")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", default="")
    REQUESTS_PER_MINUTE_LIMIT: int = int(os.getenv("REQUESTS_PER_MINUTE_LIMIT", default="600"))


config = Config()
