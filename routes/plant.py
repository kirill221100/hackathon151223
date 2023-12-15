from fastapi import APIRouter, Depends
from validation.plants import PlantData
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.plant import create_plant

plant_router = APIRouter()


@plant_router.post('/new-plant')
async def new_plant(plant_data: PlantData, session: AsyncSession = Depends(get_session)):
    return await create_plant(plant_data, session)
