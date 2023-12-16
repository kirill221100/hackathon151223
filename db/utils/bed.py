import datetime
import random
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from validation.bed import BedData
from db.models.bed import Bed
from db.utils.user import get_user_by_id
from db.utils.plant import get_plant_by_id


async def create_bed(bed_data: BedData, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    plant = await get_plant_by_id(bed_data.plant_id, session)
    bed = Bed(user=user, plant=plant, soil_type=bed_data.soil_type, soil_value=bed_data.soil_value,
              soil_humidity=bed_data.soil_humidity, watering_date=bed_data.watering_date)
    session.add(bed)
    await session.commit()
    return bed


async def get_bed_by_id(bed_id: int, session: AsyncSession):
    if res := (await session.execute(select(Bed).filter_by(id=bed_id))).scalar_one_or_none():
        return res
    raise HTTPException(404, detail='bed not found')


async def get_bed_by_id_with_plant(bed_id: int, session: AsyncSession):
    if res := (await session.execute(select(Bed).filter_by(id=bed_id).options(selectinload(Bed.plant)))).scalar_one_or_none():
        return res
    raise HTTPException(404, detail='bed not found')


async def get_beds_by_user_id(user_id: int, session: AsyncSession):
    return (await session.execute(select(Bed).filter_by(user_id=user_id).order_by(Bed.id.desc()))).scalars().all()


async def delete_bed_by_id(bed_id, user_id: int, session: AsyncSession):
    bed = await get_bed_by_id(bed_id, session)
    if bed.user_id != user_id:
        raise HTTPException(403, detail='you cant delete this bed')
    await session.delete(bed)
    await session.commit()
    return status.HTTP_200_OK


async def water_soil(bed_id: int, humidity_percent: float, user_id: int, session: AsyncSession):
    if humidity_percent > 100:
        raise HTTPException(400, detail='wrong percent')
    bed = await get_bed_by_id(bed_id, session)
    if bed.user_id != user_id:
        raise HTTPException(403, detail='you cant water this bed')
    # if bed.soil_humidity > humidity_percent:
    #     raise HTTPException(400, detail='wrong percent')
    bed.soil_humidity = humidity_percent
    bed.watering_date = datetime.datetime.now()
    await session.commit()
    return status.HTTP_200_OK


async def fertilize_soil(bed_id: int, fertilize_value: float, user_id: int, session: AsyncSession):
    bed = await get_bed_by_id(bed_id, session)
    if bed.user_id != user_id:
        raise HTTPException(403, detail='you cant fertilize this bed')
    # if bed.soil_value > fertilize_value:
    #     raise HTTPException(400, detail='wrong value')
    bed.soil_value = fertilize_value
    await session.commit()
    return status.HTTP_200_OK


async def bed_data_simulation(bed_id: int, session: AsyncSession):
    bed = await get_bed_by_id(bed_id, session)
    if bed.soil_humidity != 0 or bed.soil_value != 0:
        if bed.soil_humidity >= 0.4:
            bed.soil_humidity -= 0.4
        else:
            bed.soil_humidity = 0.0
        if bed.soil_value >= 0.2:
            bed.soil_value -= 0.2
        else:
            bed.soil_value = 0.0
        await session.commit()
    data = {'air_humidity': round(random.uniform(45, 50), 1),
            'soil_humidity': bed.soil_humidity,
            'soil_value': bed.soil_value,
            'watering_date': bed.watering_date,
            'light_level': random.randint(3500, 5000)
            }
    return data

# async def bed_data_ws(bed_id: int, ws: WebSocket, session: AsyncSession):
#     await bed_data_manager.connect(bed_id, ws)
#     bed = await get_bed_by_id(bed_id, session)
#     data_db = {'air_humidity': round(random.uniform(45, 55), 1),
#                'soil_humidity': round(bed.soil_humidity - 0.5, 1),
#                'soil_value': round(bed.soil_value - 0.3, 1),
#                'watering_date': bed.watering_date,
#                'light_level': random.randint(3500, 5000)
#                }
#     queue = asyncio.queues.Queue()
#
#     async def read_and_send_to_client(bed_id, data):
#         await bed_data_manager.send_data(bed_id, data)
#         await asyncio.sleep(2)
#
#     async def put_data(data):
#         queue.put_nowait(data)
#
#     async def get_data_and_send(bed_id):
#         data = await queue.get()
#         fetch_task = asyncio.create_task(read_and_send_to_client(bed_id, data))
#         while True:
#             data = await queue.get()
#             if not fetch_task.done():
#                 print(f'Got new data while task not complete, canceling.')
#                 fetch_task.cancel()
#             fetch_task = asyncio.create_task(read_and_send_to_client(bed_id, data))
#
#     await asyncio.gather(put_data(data_db), get_data_and_send(bed_id))
#

# bed = await get_bed_by_id(bed_id, session)
# data = {'air_humidity': round(random.uniform(45, 55), 1),
#         'soil_humidity': round(bed.soil_humidity - 0.5, 1),
#         'soil_value': round(bed.soil_value - 0.3, 1),
#         'watering_date': bed.watering_date,
#         'light_level': random.randint(3500, 5000)
#         }
# try:
#     while True:
#         received_data = await ws.receive_json()
#         print(bed.soil_humidity, data['soil_humidity'])
#         if bed.watering_date < data['watering_date']:
#             data['soil_humidity'] = bed.soil_humidity
#         else:
#             data['soil_humidity'] -= 0.5
#         await bed_data_manager.send_data(bed_id, json.dumps(data, indent=4, sort_keys=True, default=str))
#         await asyncio.sleep(1)

# await session.commit()
#         await asyncio.sleep(2)
# async def task():
#     try:
#         while True:
#             bed = await get_bed_by_id(bed_id, session)
#             bed.humidity -= 0.5
#             bed.soil_value -= 0.3
#             await session.flush()
#             data = {'air_humidity': round(random.uniform(45, 55), 1),
#                     'soil_humidity': round(bed.humidity, 1),
#                     'soil_value': round(bed.soil_value, 1),
#                     'watering_date': bed.watering_date,
#                     'light_level': random.randint(3500, 5000)
#                     }
#             await bed_data_manager.send_data(bed_id, data)
#             await asyncio.sleep(5)
#             #await session.commit()
#     except (WebSocketDisconnect, ConnectionClosedOK, asyncio.CancelledError):
#         await bed_data_manager.disconnect(bed_id, ws)
# task = asyncio.create_task(task())
# try:
#     await task
# except Exception as e:
#     print(e, 234343434)
#     task.cancel()
# async def task():
#     while True:
#         bed = await get_bed_by_id(bed_id, session)
#         data['watering_date_orig'] = bed.watering_date
#         if bed.watering_date < data['watering_date']:
#             data['soil_humidity'] = bed.soil_humidity
#         else:
#             data['soil_humidity'] -= 0.5
#         await bed_data_manager.send_data(bed_id, json.dumps(data, indent=4, sort_keys=True, default=str))
#         # await session.commit()
#         await asyncio.sleep(2)
# t = asyncio.create_task(task())
# try:
#     await t
# except Exception as e:
#     print(e, 234343434)
#     t.cancel()
#
#     await bed_data_manager.disconnect(bed_id, ws)

# except (WebSocketDisconnect, ConnectionClosedOK):
#     await bed_data_manager.disconnect(bed_id, ws)
