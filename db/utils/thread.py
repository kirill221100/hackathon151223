from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from db.models.thread import Thread
from db.models.message import Message
from validation.thread import ThreadData, ThreadDataEdit
from db.utils.user import get_user_by_id


async def create_thread(thread_data: ThreadData, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    thread = Thread(title=thread_data.title, text=thread_data.text, pictures=thread_data.pictures, user=user)
    session.add(thread)
    await session.commit()
    return thread


async def get_thread_by_id(thread_id: int, session: AsyncSession):
    if res := (await session.execute(select(Thread).filter_by(id=thread_id))).scalar_one_or_none():
        return res
    raise HTTPException(404, detail='thread not found')


async def get_thread_by_id_with_messages(thread_id: int, page: int, per_page: int, session: AsyncSession):
    limit = per_page * page
    offset = (page - 1) * per_page
    message_subquery = select(Message).filter_by(thread_id=thread_id).limit(limit).offset(offset).subquery().lateral()
    if thread := (await session.execute(select(Thread).filter_by(id=thread_id).outerjoin(message_subquery)
                                                .options(contains_eager(Thread.messages, alias=message_subquery))))\
            .unique().scalar_one_or_none():
        return thread
    raise HTTPException(404, detail='thread not found')


async def edit_thread(thread_data: ThreadDataEdit, user_id: int, session: AsyncSession):
    thread = await get_thread_by_id(thread_data.id, session)
    if thread.user_id != user_id:
        raise HTTPException(403, detail='you cant edit this thread')
    for k, v in thread_data:
        if v and k != 'id':
            setattr(thread, k, v)
    await session.commit()
    return thread


async def get_threads(page: int, per_page: int, session: AsyncSession):
    limit = per_page * page
    offset = (page - 1) * per_page
    threads = (await session.execute(select(Thread).limit(limit).offset(offset))).scalars().all()
    return threads


async def delete_thread_by_id(thread_id: int, user_id: int, session: AsyncSession):
    thread = await get_thread_by_id(thread_id, session)
    if thread.user_id != user_id:
        raise HTTPException(403, detail='you cant delete this thread')
    await session.delete(thread)
    await session.commit()
    return status.HTTP_200_OK
