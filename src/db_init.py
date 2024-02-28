from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

DB_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgresql/{config.POSTGRES_DB}"


class ApplicationBase(object):
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=config.DB_LOGS, future=True)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
