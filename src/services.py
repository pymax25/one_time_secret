import uuid

from daos import SecretDAO


class CreateSecretService:

    def __init__(self, secret_dao: SecretDAO) -> None:
        self._secret_dao = secret_dao

    def execute(self, secret: str) -> uuid:
        secret_id = self._secret_dao.create_secret(secret=secret)
        return secret_id


class GetSecretService:
    def __init__(self, secret_dao: SecretDAO) -> None:
        self._secret_dao = secret_dao

    def execute(self, secret_id: uuid) -> str:
        secret = self._secret_dao.get_secret_by_id(id=secret_id)
        return str(secret, encoding='UTF-8')
