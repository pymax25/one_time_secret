import uuid
from sqlalchemy import Column, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Secret(Base):
    __tablename__ = "secret"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    token = Column(String)
    salt = Column(String)
    is_used = Column(Boolean, default=False)
