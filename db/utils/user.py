from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from security.password import verify_pass, hash_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from validation.auth import UserAuth
from db.models.user import User


async def create_user(user_data: UserAuth, session: AsyncSession):
    user = User(username=user_data.username, hashed_password=hash_password(user_data.password))
    session.add(user)
    await session.commit()
    await session.flush()
    return {'username': user_data.username, 'id': user.id}


async def login_user(user_data: OAuth2PasswordRequestForm, session: AsyncSession):
    if user := await get_user_by_username(user_data.username, session):
        if verify_pass(user_data.password, user.hashed_password):
            return {'username': user_data.username, 'id': user.id}
    raise HTTPException(status_code=401, detail='incorrect password or username',
                        headers={"WWW-Authenticate": "Bearer"})


async def get_user_by_username(username: str, session: AsyncSession):
    return (await session.execute(select(User).filter_by(username=username))).scalar_one_or_none()


async def get_user_by_id(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id))).scalar_one_or_none()

