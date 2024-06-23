from typing import List, Sequence

from fastapi import Depends
from sqlalchemy import RowMapping

from models.BaseModel import AbstractMap
from models.maps import ZU
from repositories.maps import MapRepository
from schemas.map import Marker, CreateCommentOpts, FilterOpts, FilterRequest
from utils.constant import EXCLUDED_TABLES
from utils.utils import map_name_to_class
import models.maps as maps_models


class MapService:
    def __init__(self, repository: MapRepository = Depends()):
        self._repo = repository
        self._mn_to_cl = map_name_to_class(maps_models)

    async def get_map_markers(self, class_maps: List[AbstractMap]) -> List[Marker]:
        markers = []
        for class_map in class_maps:
            result = await self._repo.get_map(class_map)
            map_markers = [self._create_marker(row, class_map) for row in result]
            markers.extend(map_markers)

        return markers

    async def search_by_cadastra(self, cadastra: str) -> Marker:
        result = await self._repo.search_by_cadastra(cadastra)
        return self._create_marker(result, ZU())

    async def search_by_address(self, address: str) -> List[Marker]:
        results = await self._repo.search_by_address(address)
        markers = []
        for row in results:
            map_marker = self._create_marker(row, ZU())
            markers.append(map_marker)

        return markers

    async def create_comment(self, opts: CreateCommentOpts):
        await self._repo.create_comment(opts)

    async def get_available_maps(self) -> Sequence[str]:
        map_names = await self._repo.get_available_maps()

        map_names = [table for table in map_names if table not in EXCLUDED_TABLES]

        return map_names

    async def get_map_columns(self, map: str) -> List[str]:
        model_map = self._mn_to_cl[map]

        columns = model_map.__table__.columns
        columns = [str(column).split(".")[1] for column in columns]
        return columns

    async def get_records_for_exporter(
        self, fields: List[str], model_class: AbstractMap, gids: List[int]
    ):
        return await self._repo.get_records_for_exporter(fields, model_class, gids)

    async def filters(self, opts: FilterRequest):
        map_model = self._mn_to_cl[opts.class_name]
        results = await self._repo.filters(map_model, FilterOpts(filters=opts.filters))

        markers = []
        for row in results:
            markers.append(self._create_marker(row, map_model))

        return markers

    async def maps_intersection(self, maps: List[str]) -> List[AbstractMap]:
        class_maps = []
        for map in maps:
            class_maps.append(self._mn_to_cl[map])

        results = await self._repo.maps_intersection(*class_maps)

        return results

    async def get_dashboard(self):
        results = await self._repo.get_dashboard()

        return results

    async def long_narrow_layers(self, maps: List[str], threshold_ratio: float) -> List[Marker]:
        markers = []
        for map in maps:
            class_map = self._mn_to_cl[map]
            result = await self._repo.get_long_narrow_layers(class_map, threshold_ratio)
            map_markers = [self._create_marker(row, class_map) for row in result]
            markers.extend(map_markers)

        return markers

    def _create_marker(self, row: dict | RowMapping, map_model: AbstractMap) -> Marker:
        popup_text = map_model.get_popup(row)
        marker = Marker(
            gid=row["gid"],
            lat=row["lat"],
            lon=row["lon"],
            geom=row["geom"],
            popup=popup_text,
            map_name=map_model.__tablename__,
        )

        return marker
