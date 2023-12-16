import datetime
from typing import Optional
from validation.plants import PLantResponse
from pydantic import BaseModel, Field
import enum


class SoilDefaultValues(enum.Enum):
    #  мг-экв/100 г почвы
    sod_podzolic = 5
    grey_forest = 23
    chernozem = 55
    light_chestnut = 30
    red_soil = 18
    gray_soil = 14


class SoilTypes(enum.Enum):
    sod_podzolic = 'sod-podzolic'
    grey_forest = 'grey forest'
    chernozem = 'chernozem'
    light_chestnut = 'light-chestnut'
    red_soil = 'red soil'
    gray_soil = 'gray soil'


class BedData(BaseModel):
    plant_id: int
    soil_type: SoilTypes
    soil_value: float
    soil_humidity: float = Field(ge=0, le=100)
    watering_date: Optional[datetime.datetime] = None


class BedResponse(BedData):
    id: int
    plant_id: int
    user_id: int


class NewBedResponse(BedResponse):
    plant: PLantResponse


class BedDataSimulation(BaseModel):
    air_humidity: float
    soil_humidity: float
    soil_value: float
    watering_date: Optional[datetime.datetime]
    light_level: int


class WaterSoil(BaseModel):
    bed_id: int
    humidity_percent: float = Field(gt=0, le=100)


class FertilizeSoil(BaseModel):
    bed_id: int
    fertilize_value: float
