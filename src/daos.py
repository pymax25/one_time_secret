import base64
import uuid

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from entities import SecretEntity
from exceptions import SecretNotFound
from models import Secret


class SecretDAO:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_entity(self, secret: Secret) -> SecretEntity:
        return SecretEntity(
            id=secret.id,
            salt=secret.salt,
            token=secret.token,
        )

    def get_secret_by_id(self, id: uuid) -> str:
        secret = self._db.query(Secret).filter(Secret.id == id).first()
        if not secret:
            raise SecretNotFound

        secret_entity = self._to_entity(secret=secret)
        key = base64.b64decode(secret_entity.salt.encode())
        f = Fernet(key=key)
        token = base64.b64decode(secret_entity.token.encode())
        secret_str = f.decrypt(token)
        self._db.delete(secret)
        self._db.commit()
        return secret_str

    def create_secret(self, secret: str) -> uuid:
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(secret.encode())
        secret = Secret(
            token=base64.b64encode(token).decode('utf-8'),
            salt=base64.b64encode(key).decode('utf-8')
        )
        self._db.add(secret)
        self._db.commit()
        return secret.id
