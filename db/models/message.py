import datetime
from sqlalchemy import Integer, Column, String, Enum, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_setup import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')
    thread_id = Column(Integer, ForeignKey('threads.id'))
    thread = relationship('Thread', back_populates='messages')
    pictures = Column(ARRAY(String), server_default='{}')
    date = Column(DateTime, default=datetime.datetime.now)
