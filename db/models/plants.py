from sqlalchemy import Integer, Column, String, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from validation.plants import PlantType
from db.db_setup import Base


class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    beds = relationship('Bed', back_populates='plant')
    type = Column(Enum(PlantType))
    picture = Column(String)
    description = Column(String)
    recommended_humidity = Column(Float)  # в процентах
    recommended_light_level = Column(Integer)  # в лк

