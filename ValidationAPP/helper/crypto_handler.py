from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib

from fastapi import HTTPException

BLOCK_SIZE: int = 16
encoding: str = "UTF-8"


def convert_to_hash(secret_key: str) -> bytes:
    key: bytes = secret_key.encode()
    hashed_key: bytes = hashlib.sha256(key).digest()
    return hashed_key


def encrypt(data_to_be_encrypted: str, secret_key: str) -> bytes:
    hashed_key: bytes = convert_to_hash(secret_key)
    IV: bytes = Random.new().read(BLOCK_SIZE)
    aes: AES = AES.new(hashed_key, AES.MODE_CFB, IV)
    return base64.b64encode(IV + aes.encrypt(data_to_be_encrypted.encode(encoding)))


def decrypt(encrypted: str, secret_key: str) -> str:
    try:
        encrypted: bytes = bytes(encrypted, encoding)
        secret_key = convert_to_hash(secret_key)
        encrypted: bytes = base64.b64decode(encrypted.decode(encoding))
        IV: bytes = encrypted[:BLOCK_SIZE]
        aes: AES = AES.new(secret_key, AES.MODE_CFB, IV)
        return aes.decrypt(encrypted[BLOCK_SIZE:]).decode(encoding)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data")
