import datetime
from typing import Optional

from pydantic import BaseModel
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
    sod_podzolic = 'дерново-подзолистая'
    grey_forest = 'серая лесная'
    chernozem = 'чернозём'
    light_chestnut = 'светло-каштановая'
    red_soil = 'краснозём'
    gray_soil = 'серозём'


class BedData(BaseModel):
    plant_id: int
    soil_type: SoilTypes
    soil_value: float
    soil_humidity: float


class BedDataSimulation(BaseModel):
    air_humidity: float
    soil_humidity: float
    soil_value: float
    watering_date: Optional[datetime.datetime]
    light_level: int

