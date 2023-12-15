from security.config import get_config
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, WebSocketException, status

config = get_config()


def create_access_token(data: dict):
    exp = datetime.now() + timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = data.copy()
    token.update({'exp': exp})
    return jwt.encode(token, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)


def create_refresh_token(data: dict):
    exp = datetime.now() + timedelta(config.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = data.copy()
    token.update({'exp': exp})
    return jwt.encode(token, config.JWT_REFRESH_SECRET_KEY, algorithm=config.ALGORITHM)


def verify_token(token: str):
    try:
        user_data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        if user_data:
            return user_data
        raise HTTPException(status_code=401, detail='empty token', headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail='invalid token', headers={"WWW-Authenticate": "Bearer"})


def verify_token_ws(token: str):
    try:
        user_data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        if user_data:
            return user_data
        raise WebSocketException(status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise WebSocketException(status.HTTP_401_UNAUTHORIZED)
