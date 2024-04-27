from pydantic import BaseModel


class Playlists(BaseModel):
    user_id: int
    name: str
    tracks: str
