from pydantic import BaseModel


class SelectedObject(BaseModel):
    gid: int
    map_name: str
