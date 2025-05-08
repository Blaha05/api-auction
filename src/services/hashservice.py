from typing import Union
import bcrypt

class HashedPassword:

    @staticmethod
    def hashed_password(password: str) -> bytes:
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed

    @staticmethod
    def check_password(password: str, hashed_password: Union[str, bytes]) -> bool:
        password = password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        res = bcrypt.checkpw(password, hashed_password)
        return res
