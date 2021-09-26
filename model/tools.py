from typing import Union
import base64
import secrets
import hashlib
import hmac


def drop_none(obj):
    return {k: v for k, v in obj.items() if v is not None}


def urlsafe_b64dumps(value: Union[str, bytes]) -> str:
    value = value.encode('ascii') if isinstance(value, str) else value
    return base64.urlsafe_b64encode(value).decode('ascii')

def urlsafe_b64loads(value: str) -> bytes:
    value = value.encode('ascii') if isinstance(value, str) else value
    return base64.urlsafe_b64encode(value).decode('ascii')

class SecretToken:

    @classmethod
    def gen(cls, n: int):
        return cls(secrets.token_urlsafe(n)[:n])

    def __init__(self, secret: Union[str, bytes]):
        self._secret = secret if isinstance(secret, str) else secret.decode('ascii')

    def __len__(self):
        return len(self._secret)

    def __str__(self):
        return self._secret

    def __bytes__(self):
        return self._secret.encode('ascii')

    @property
    def hash(self):
        return hashlib.md5(str(self).encode('ascii')).digest()

    def __eq__(self, secret_hash: bytes):
        return hmac.compare_digest(self.hash, secret_hash)
