from typing import Any
from bcrypt import (hashpw, gensalt, checkpw)


def encrypt_data(data) -> str:
    raw_data = hashpw(data.encode(), gensalt())
    hashed_data = raw_data.decode()

    return hashed_data


def check_encrypted_data(data, hashed_data) -> bool:
    checked_data = checkpw(data, hashed_data)

    return checked_data
