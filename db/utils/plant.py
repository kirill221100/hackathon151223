from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models.plants import Plant
from validation.plants import PlantData


async def create_plant(plant_data: PlantData, session: AsyncSession):
    plant = Plant(name=plant_data.name, type=plant_data.type, recommended_humidity=plant_data.recommended_humidity)
    session.add(plant)
    await session.commit()
    return plant


async def get_plant_by_id(plant_id: int, session: AsyncSession):
    return (await session.execute(select(Plant).filter_by(id=plant_id))).scalar_one_or_none()
