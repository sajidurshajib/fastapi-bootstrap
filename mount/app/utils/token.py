from fastapi import status
from datetime import datetime, timedelta
from typing import Optional
from app.services.config import config
from jose import jwt, JWTError, ExpiredSignatureError
from app.schemas.tokens import TokenData


class Token:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime() + expires_delta
        else:
            expire = datetime.datetime() + timedelta(days=2)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def validate_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM], options={"verify_sub": False})
            user_id = payload.get("sub")

            if user_id is None:
                raise status.HTTP_404_NOT_FOUND
            token_data = TokenData(user_id=user_id)
            return token_data

        except ExpiredSignatureError:
            raise status.HTTP_404_NOT_FOUND
        except JWTError as err:
            print(err)
            raise status.HTTP_404_NOT_FOUND

