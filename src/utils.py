import base64
import uuid
from typing import Any

from cryptography.fernet import Fernet


def is_valid_uuid(value: Any):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def encrypt_secret(secret: str) -> tuple:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    token = base64.b64encode(fernet.encrypt(secret.encode())).decode('utf-8')
    salt = base64.b64encode(key).decode('utf-8')
    return token, salt


def decrypt_secret(key: str, token: str) -> str:
    key = base64.b64decode(key.encode())
    f = Fernet(key=key)
    token = base64.b64decode(token.encode())
    secret_bytes = f.decrypt(token)
    return str(secret_bytes, encoding="UTF-8")
