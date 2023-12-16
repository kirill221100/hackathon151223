from fastapi import APIRouter, Depends, status
from typing import List
from validation.bed import BedData, BedDataSimulation, BedResponse, NewBedResponse
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.bed import create_bed, water_soil, fertilize_soil, bed_data_simulation, delete_bed_by_id, get_bed_by_id, \
    get_beds_by_user_id, get_bed_by_id_with_plant, get_beds_by_user_id_with_plant

bed_router = APIRouter()


@bed_router.post('/new-bed', response_model=NewBedResponse)
async def new_bed(bed_data: BedData, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await create_bed(bed_data, user['id'], session)


@bed_router.patch('/water-soil/{bed_id}', status_code=status.HTTP_200_OK)
async def water_soil_path(bed_id: int, humidity_percent: float, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await water_soil(bed_id, humidity_percent, user['id'], session)


@bed_router.patch('/fertilize-soil/{bed_id}', status_code=status.HTTP_200_OK)
async def fertilize_soil_path(bed_id: int, fertilize_value: float, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await fertilize_soil(bed_id, fertilize_value, user['id'], session)


@bed_router.delete('/delete-bed-by-id/{bed_id}', status_code=status.HTTP_200_OK)
async def delete_bed_by_id_path(bed_id: int, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await delete_bed_by_id(bed_id, user['id'], session)


@bed_router.get('/get-beds-by-user-id', response_model=List[NewBedResponse])
async def get_beds_by_user_id_path(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await get_beds_by_user_id_with_plant(user['id'], session)


@bed_router.get('/get-bed-by-id/{bed_id}', response_model=NewBedResponse)
async def get_bed_by_id_path(bed_id: int, session: AsyncSession = Depends(get_session)):
    return await get_bed_by_id_with_plant(bed_id, session)


@bed_router.patch('/bed-data-simulation/{bed_id}', response_model=BedDataSimulation)
async def bed_data_simulation_path(bed_id: int, session: AsyncSession = Depends(get_session)):
    return await bed_data_simulation(bed_id, session)
