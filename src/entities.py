from dataclasses import dataclass


@dataclass
class SecretEntity:
    id: int
    token: str
    salt: str
