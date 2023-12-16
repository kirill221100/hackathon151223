from fastapi import APIRouter, Depends, WebSocket, status
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from validation.message import MessageData, MessageResponse, MessageEdit
from db.utils.message import create_message, new_message_ws, get_message_by_id, edit_message, delete_message_by_id

message_router = APIRouter()


@message_router.post('/new-message', response_model=MessageResponse)
async def new_message_path(message_data: MessageData, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await create_message(message_data, user['id'], session)


@message_router.get('/get-message-by-id/{message_id}', response_model=MessageResponse)
async def get_message_by_id_path(message_id: int, session: AsyncSession = Depends(get_session)):
    return await get_message_by_id(message_id, session)


@message_router.patch('/edit-message', response_model=MessageResponse)
async def edit_message_path(message_data: MessageEdit, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await edit_message(message_data, user['id'], session)


@message_router.delete('/delete-message/{message_id}', status_code=status.HTTP_200_OK)
async def delete_message_path(message_id: int, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await delete_message_by_id(message_id, user['id'], session)


@message_router.websocket('/new-message-ws/{thread_id}')
async def mew_message_ws(ws: WebSocket, thread_id: int):
    await new_message_ws(ws, thread_id)