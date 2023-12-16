from pydantic import BaseModel, Field
from typing import Optional
import enum


class PlantType(enum.Enum):
    fruit = 'фрукт'
    vegetable = 'овощ'
    tree = 'дерево'
    other = 'другое'


class PlantData(BaseModel):
    name: str
    type: PlantType
    picture: str
    description: str
    recommended_humidity: float = Field(gt=0, le=100)
    recommended_light_level: int = Field(gt=0, le=10000)


class PLantResponse(PlantData):
    id: int


class PlantDataEdit(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[PlantType] = None
    picture: Optional[str] = None
    description: Optional[str] = None
    recommended_humidity: Optional[float] = Field(None, gt=0, le=100)
    recommended_light_level: Optional[int] = Field(None, gt=0, le=10000)


# class SoilDefaultValues(enum.Enum):
#     #  мг-экв/100 г почвы
#     cucumber = 'огурец'
#     cauliflower = 'цветная капуста'
#     turnip = 'репа'
#     radish = 'редька'
#     lettuce = 'салат'
#     onion = 'лук'
#     garlic = 'чеснок'
#     beet = 'свекла'
#     pumpkin = 'тыква'
#     zucchini = 'кабачок'
#     pepper = 'перец'
#     bean = 'фасоль'
#     pea = 'горох'
#     carrot = 'морковь'
#     tomato = 'помидор'
#     eggplant = 'баклажан'
#     parsley = 'петрушка'
#
#
# class Vegetables(BaseModel):
#     cucumber = 'огурец'
#     cauliflower = 'цветная капуста'
#     turnip = 'репа'
#     radish = 'редька'
#     lettuce = 'салат'
#     onion = 'лук'
#     garlic = 'чеснок'
#     beet = 'свекла'
#     pumpkin = 'тыква'
#     zucchini = 'кабачок'
#     pepper = 'перец'
#     bean = 'фасоль'
#     pea = 'горох'
#     carrot = 'морковь'
#     tomato = 'помидор'
#     eggplant = 'баклажан'
#     parsley = 'петрушка'