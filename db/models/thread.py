import datetime
from sqlalchemy import Integer, Column, String, Enum, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_setup import Base


class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='threads')
    messages = relationship('Message', back_populates='thread')
    pictures = Column(ARRAY(String), server_default='{}')
    date = Column(DateTime, default=datetime.datetime.now)
