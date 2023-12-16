from fastapi import APIRouter, Depends, status
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from validation.thread import ThreadData, ThreadDataEdit, ThreadResponse, ThreadResponseWithMessages
from db.utils.thread import create_thread, get_thread_by_id, get_thread_by_id_with_messages, edit_thread, delete_thread_by_id

thread_router = APIRouter()


@thread_router.post('/new-thread', response_model=ThreadResponse)
async def new_thread_path(thread_data: ThreadData, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await create_thread(thread_data, user['id'], session)


@thread_router.patch('/edit-thread', response_model=ThreadResponse)
async def edit_thread_path(thread_data: ThreadDataEdit, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await edit_thread(thread_data, user['id'], session)


@thread_router.get('/get-thread-by-id/{thread_id}', response_model=ThreadResponse)
async def get_thread_by_id_path(thread_id: int, session: AsyncSession = Depends(get_session)):
    return await get_thread_by_id(thread_id, session)


@thread_router.get('/get-thread-by-id-with-messages/{thread_id}', response_model=ThreadResponseWithMessages)
async def get_thread_by_id_with_messages_path(thread_id: int, page: int = 1, per_page: int = 10, session: AsyncSession = Depends(get_session)):
    return await get_thread_by_id_with_messages(thread_id, page, per_page, session)


@thread_router.delete('/delete-thread-by-id/{thread_id}', status_code=status.HTTP_200_OK)
async def delete_thread_path(plant_id: int, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await delete_thread_by_id(plant_id, user['id'], session)
