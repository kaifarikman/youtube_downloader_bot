from bot.db.models.playlists import Playlists
from bot.db.schemas.playlists import Playlists as PlaylistsDB
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from bot.db.db import engine


def create_playlist(playlist: Playlists):
    session = sessionmaker(engine)()
    playlist_db = PlaylistsDB(
        user_id=playlist.user_id,
        name=playlist.name,
        tracks=playlist.tracks
    )
    session.add(playlist_db)
    session.commit()


def get_playlist_id(playlist_name: str, user_id: int):
    session = sessionmaker(engine)()
    query = session.query(PlaylistsDB).filter_by(
        name=playlist_name, user_id=user_id
    )
    return query.first().id


def get_playlist(playlist_name: str, user_id: int):
    session = sessionmaker(engine)()
    query = session.query(PlaylistsDB).filter_by(
        name=playlist_name, user_id=user_id
    )
    if query.count() > 0:
        return False
    return True


def get_user_playlists(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(PlaylistsDB).filter_by(
        user_id=user_id
    )
    return query.all()


def add_track_by_id(user_id: int, playlist_id: int, track_id: str):
    session = sessionmaker(engine)()
    query = session.query(PlaylistsDB).filter_by(
        id=playlist_id,
        user_id=user_id
    )
    tracks = str(query.first().tracks)
    tracks += " " + track_id
    tracks = tracks.lstrip().rstrip()
    update_data(playlist_id, tracks)


def update_data(playlist_id: int, tracks: str):
    session = sessionmaker(engine)()
    playlist = session.query(PlaylistsDB).filter_by(
        id=playlist_id
    ).first()
    playlist.tracks = tracks
    session.commit()


def get_playlist_tracks(playlist_id: int):
    session = sessionmaker(engine)()
    playlist = session.query(PlaylistsDB).filter_by(
        id=playlist_id,
    ).first()
    return str(playlist.tracks)
