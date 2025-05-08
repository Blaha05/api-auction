from fastapi import HTTPException, status
from jose import JWTError
import jwt
from datetime import datetime, timedelta

class Token:

    def __init__(self, key:str, time:int, algorithm:str):
        self.key = key
        self.time = time
        self.algorithm = algorithm

    def create_token(self, data:dict):
        expire = datetime.utcnow() + timedelta(minutes=self.time)
        data.update({'exp': expire})
        token = jwt.encode(data, self.key)
        return token

    def decode_token(self, token):
        try:
            decode = jwt.decode(token, self.key, self.algorithm)
            return decode
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

