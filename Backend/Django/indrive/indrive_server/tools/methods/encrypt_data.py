from typing import Any
from bcrypt import (hashpw, gensalt)


def encrypt_data(data: Any) -> str:
    raw_data = hashpw(data.encode('utf-8'), gensalt())
    hashed_password = raw_data.decode('utf-8')

    return hashed_password
