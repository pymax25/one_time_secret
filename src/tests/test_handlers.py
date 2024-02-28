from unittest.mock import patch

import pytest

from main import app
from services import CreateSecretService, GetSecretService
from tests.data_for_tests import invalid_uuid, valid_uuid


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create_secret_valid_data(client):
    with patch.object(CreateSecretService, 'execute') as mock_execute:
        client.post('/secret', json={"secret": "test_secret"})
        mock_execute.assert_called_once_with(secret='test_secret')


def test_create_secret_invalid_data(client):
    response = client.post('/secret', json={})
    assert response.status_code == 400


def test_get_secret_valid_uuid(client):
    with patch.object(GetSecretService, 'execute') as mock_execute:
        client.post(f'/secret/{valid_uuid}')
        mock_execute.assert_called_once_with(secret_id='6ba7b810-9dad-11d1-80b4-00c04fd430c8')


def test_get_secret_invalid_uuid(client):
    response = client.post(f'/secret/{invalid_uuid}')
    assert response.status_code == 400
