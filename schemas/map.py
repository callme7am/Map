from typing import Dict, Any

from pydantic import BaseModel, validator, field_validator

from models.BaseModel import AbstractMap


class CreateCommentOpts(BaseModel):
    gid: int
    comment: str


class SearchListOpts(BaseModel):
    cadastra: str


class FilterRequest(BaseModel):
    class_name: str
    filters: Dict[str, Any]


class FilterOpts(BaseModel):
    filters: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


class Marker(BaseModel):
    lat: float
    lon: float
    gid: int
    geom: str
    popup: str
    map_name: str | None = None
