from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from validation.auth import UserAuth
from security.jwt import create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.user import create_user, login_user

auth_router = APIRouter()


@auth_router.post('/register')
async def register_path(reg_data: UserAuth, session: AsyncSession = Depends(get_session)):
    data = await create_user(reg_data, session)
    return {'access_token': create_access_token(data), 'refresh_token': create_refresh_token(data),
            'token_type': 'bearer'}


@auth_router.post('/login')
async def login_path(login_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    data = await login_user(user_data=login_data, session=session)
    return {'access_token': create_access_token(data), 'refresh_token': create_refresh_token(data),
            'token_type': 'bearer'}

