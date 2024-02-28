from unittest.mock import Mock

from services import CreateSecretService, GetSecretService


def test_create_secret():
    mock_secret_dao = Mock()
    mock_secret_dao.create_secret.return_value = '12345678-90ab-cdef-ghij-klmnopqrstuvwxyz'
    mock_logger = Mock()

    service = CreateSecretService(secret_dao=mock_secret_dao, logger=mock_logger)

    result = service.execute('my secret')

    assert result == '12345678-90ab-cdef-ghij-klmnopqrstuvwxyz'
    mock_secret_dao.create_secret.assert_called_once_with(secret='my secret')


def test_get_secret():
    mock_secret_dao = Mock()
    mock_secret_dao.get_secret_by_id.return_value = 'my secret'
    mock_logger = Mock()

    service = GetSecretService(secret_dao=mock_secret_dao, logger=mock_logger)

    result = service.execute('12345678-90ab-cdef-ghij-klmnopqrstuvwxyz')

    assert result == 'my secret'
    mock_secret_dao.get_secret_by_id.assert_called_once_with(id='12345678-90ab-cdef-ghij-klmnopqrstuvwxyz')
