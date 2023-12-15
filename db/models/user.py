from sqlalchemy import Integer, Column, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_setup import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    beds = relationship('Bed', back_populates='user')
