from bot.db.db import Base
from sqlalchemy import Column, Integer, String


class Tracks(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String)
