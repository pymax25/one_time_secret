import uuid
from logging import Logger

from daos import SecretDAO


class CreateSecretService:
    def __init__(self, secret_dao: SecretDAO, logger: Logger) -> None:
        self._secret_dao = secret_dao
        self._logger = logger

    def execute(self, secret: str) -> uuid:
        self._logger.info("Trying to create new secret...")
        secret_id = self._secret_dao.create_secret(secret=secret)
        self._logger.info(f"New secret with id {secret_id} created!")
        return secret_id


class GetSecretService:
    def __init__(self, secret_dao: SecretDAO, logger: Logger) -> None:
        self._secret_dao = secret_dao
        self._logger = logger

    def execute(self, secret_id: uuid) -> str:
        self._logger.info(f"Trying to get secret by id {secret_id}")
        secret = self._secret_dao.get_secret_by_id(id=secret_id)
        self._logger.info(f"Secret with id {secret_id} found")
        return secret
