from typing import Any
from bcrypt import (hashpw, gensalt, checkpw)


def encrypt_data(data: bytes) -> str:
    raw_data = hashpw(data.encode('utf-8'), gensalt())
    hashed_data = raw_data.decode('utf-8')

    return hashed_data


def check_encrypted_data(data: bytes, hashed_data: bytes) -> bool:
    checked_data = checkpw(data, hashed_data)

    return checked_data
