from sqlalchemy import Integer, Column, String, Enum, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from validation.bed import SoilTypes
from db.db_setup import Base


class Bed(Base):
    __tablename__ = 'beds'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='beds')
    plant_id = Column(Integer, ForeignKey('plants.id'))
    plant = relationship('Plant', back_populates='beds')
    soil_type = Column(Enum(SoilTypes))
    soil_value = Column(Float)
    watering_date = Column(DateTime)
    soil_humidity = Column(Float)  # в процентах

