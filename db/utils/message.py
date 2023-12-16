from fastapi import HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from validation.message import MessageData, MessageResponse, MessageEdit
from db.models.message import Message
from db.utils.thread import get_thread_by_id
from utils.ws import message_manager
from db.utils.user import get_user_by_id


async def create_message(message_data: MessageData, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    message = await get_thread_by_id(message_data.thread_id, session)
    message = Message(text=message_data.text, pictures=message_data.pictures, user=user, thread=message)
    session.add(message)
    await session.commit()
    await message_manager.send_data(message_data.thread_id, jsonable_encoder(MessageResponse.model_validate(jsonable_encoder(message))))
    return message


async def get_message_by_id(message_id: int, session: AsyncSession):
    return (await session.execute(select(Message).filter_by(id=message_id))).scalar_one_or_none()


async def edit_message(message_data: MessageEdit, user_id: int, session: AsyncSession):
    message = await get_message_by_id(message_data.id, session)
    if message.user_id != user_id:
        raise HTTPException(403, detail='you cant edit this message')
    for k, v in message_data:
        if v and k != 'id':
            setattr(message, k, v)
    await session.commit()
    await message_manager.send_data(message.thread_id,
                                    jsonable_encoder(MessageResponse.model_validate(jsonable_encoder(message))))
    return message


async def delete_message_by_id(message_id: int, user_id: int, session: AsyncSession):
    message = await get_message_by_id(message_id, session)
    if message.user_id != user_id:
        raise HTTPException(403, detail='you cant delete this message')
    await session.delete(message)
    await session.commit()
    return status.HTTP_200_OK


async def new_message_ws(ws: WebSocket, thread_id: int):
    await message_manager.connect(thread_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            await message_manager.send_data(thread_id, data)
    except WebSocketDisconnect:
        await message_manager.disconnect(thread_id, ws)
