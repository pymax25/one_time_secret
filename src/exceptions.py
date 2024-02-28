class BaseOneTimeSecretException(Exception):
    pass


class SecretNotFound(BaseOneTimeSecretException):
    pass
