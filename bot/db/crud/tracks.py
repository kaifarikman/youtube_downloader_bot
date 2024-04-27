from bot.db.models.tracks import Tracks
from bot.db.schemas.tracks import Tracks as TracksDB
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from bot.db.db import engine


def create_track(track: Tracks):
    session = sessionmaker(engine)()
    track_db = TracksDB(
        file_id=track.file_id,
    )
    session.add(track_db)
    session.commit()


def get_track_by_file_id(file_id: str):
    session = sessionmaker(engine)()
    query = session.query(TracksDB).filter_by(
        file_id=file_id
    ).first()
    return str(query.id)


def get_track_by_track_id(track_id: str):
    track_id = int(track_id)
    session = sessionmaker(engine)()
    query = session.query(TracksDB).filter_by(
        id=track_id
    ).first()
    return str(query.file_id)
