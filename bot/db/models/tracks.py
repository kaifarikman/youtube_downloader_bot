from pydantic import BaseModel


class Tracks(BaseModel):
    file_id: str
