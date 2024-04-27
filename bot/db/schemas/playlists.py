from bot.db.db import Base
from sqlalchemy import Column, Integer, String


class Playlists(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(String)
    tracks = Column(String)
