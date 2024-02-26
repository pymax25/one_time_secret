import uuid

from sqlalchemy.orm import Session

from entities import SecretEntity
from exceptions import SecretNotFound
from models import Secret
from utils import decrypt_secret, encrypt_secret


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
        secret_str = decrypt_secret(key=secret_entity.salt, token=secret_entity.token)
        self._db.delete(secret)
        self._db.commit()
        return secret_str

    def create_secret(self, secret: str) -> uuid:
        token, salt = encrypt_secret(secret=secret)
        secret = Secret(
            token=token,
            salt=salt,
        )
        self._db.add(secret)
        self._db.commit()
        return secret.id
