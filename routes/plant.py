from fastapi import APIRouter, Depends
from validation.plants import PlantData, PlantDataEdit
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.plant import create_plant, edit_plant, get_plant_by_id, delete_plant_by_id

plant_router = APIRouter()


@plant_router.post('/new-plant')
async def new_plant_path(plant_data: PlantData, session: AsyncSession = Depends(get_session)):
    return await create_plant(plant_data, session)


@plant_router.patch('/edit-plant')
async def edit_plant_path(plant_data: PlantDataEdit, session: AsyncSession = Depends(get_session)):
    return await edit_plant(plant_data, session)


@plant_router.get('/get-plant-by-id/{plant_id}')
async def get_plant_path(plant_id: int, session: AsyncSession = Depends(get_session)):
    return await get_plant_by_id(plant_id, session)


@plant_router.delete('/delete-plant-by-id/{plant_id}')
async def delete_plant_path(plant_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_plant_by_id(plant_id, session)
