from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.models.plants import Plant
from validation.plants import PlantData, PlantDataEdit


async def create_plant(plant_data: PlantData, session: AsyncSession):
    try:
        plant = Plant(name=plant_data.name, type=plant_data.type, recommended_humidity=plant_data.recommended_humidity)
        session.add(plant)
        await session.commit()
        return plant
    except IntegrityError:
        raise HTTPException(400, detail='name already exists')


async def get_plant_by_id(plant_id: int, session: AsyncSession):
    if res := (await session.execute(select(Plant).filter_by(id=plant_id))).scalar_one_or_none():
        return res
    raise HTTPException(404, detail='plant not found')


async def delete_plant_by_id(plant_id: int, session: AsyncSession):
    plant = await get_plant_by_id(plant_id, session)
    await session.delete(plant)
    await session.commit()
    return status.HTTP_200_OK


async def edit_plant(plant_data: PlantDataEdit, session: AsyncSession):
    plant = await get_plant_by_id(plant_data.id, session)
    for k, v in plant_data:
        if v and k != 'id':
            setattr(plant, k, v)
    await session.commit()
    return plant
