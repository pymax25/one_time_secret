from tests.data_for_tests import invalid_uuid, valid_uuid
from utils import decrypt_secret, encrypt_secret, is_valid_uuid


def test_is_valid_uuid():
    assert is_valid_uuid(valid_uuid)
    assert not is_valid_uuid(invalid_uuid)


def test_encrypt_decrypt_secret():
    secret = "Test secret"
    token, salt = encrypt_secret(secret)
    decrypted_secret = decrypt_secret(salt, token)
    assert decrypted_secret == secret
