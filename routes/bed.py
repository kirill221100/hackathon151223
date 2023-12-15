from fastapi import APIRouter, Depends, WebSocket
from validation.bed import BedData, BedDataSimulation
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.bed import create_bed, water_soil, fertilize_soil, bed_data_simulation

bed_router = APIRouter()


@bed_router.post('/new-bed')
async def new_bed(bed_data: BedData, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await create_bed(bed_data, user['id'], session)


@bed_router.patch('/water-soil/{bed_id}')
async def water_soil_path(bed_id: int, humidity_percent: float, session: AsyncSession = Depends(get_session)):
    return await water_soil(bed_id, humidity_percent, session)


@bed_router.patch('/fertilize-soil/{bed_id}')
async def fertilize_soil_path(bed_id: int, fertilize_value: float, session: AsyncSession = Depends(get_session)):
    return await fertilize_soil(bed_id, fertilize_value, session)


@bed_router.patch('/bed-data-simulation/{bed_id}', response_model=BedDataSimulation)
async def bed_data_simulation_path(bed_id: int, session: AsyncSession = Depends(get_session)):
    return await bed_data_simulation(bed_id, session)
