from pydantic import BaseModel
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
    recommended_humidity: float
    recommended_light_level: int


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