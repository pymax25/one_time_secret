import uuid
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from daos import SecretDAO
from exceptions import SecretNotFound
from models import Secret


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def secret_dao(mock_db):
    return SecretDAO(db=mock_db)


def test_get_secret_by_id_found(mock_db):
    from utils import encrypt_secret

    secret_dao = SecretDAO(db=mock_db)
    secret_id = uuid.uuid4()
    token, salt = encrypt_secret("test_secret")
    secret = Secret(id=secret_id, salt=salt, token=token)
    mock_db.query().filter().first.return_value = secret

    result = secret_dao.get_secret_by_id(secret_id)

    assert result == "test_secret"
    mock_db.delete.assert_called_once_with(secret)
    mock_db.commit.assert_called_once()


def test_get_secret_by_id_not_found(mock_db):
    secret_dao = SecretDAO(db=mock_db)
    secret_id = uuid.uuid4()
    mock_db.query().filter().first.return_value = None

    with pytest.raises(SecretNotFound):
        secret_dao.get_secret_by_id(secret_id)


def test_create_secret(mock_db):
    secret_dao = SecretDAO(db=mock_db)
    secret = "test_secret"

    secret_dao.create_secret(secret)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
