from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = f"postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@postgresql/{Config.POSTGRES_DB}"


class ApplicationBase(object):
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=True, future=True)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)