import time
from typing import Sequence, List

from fastapi import Depends
from geoalchemy2.functions import (
    ST_X,
    ST_Centroid,
    ST_AsGeoJSON,
    ST_Y,
    ST_Intersects,
    ST_IsEmpty,
    ST_Intersection, ST_Width, ST_Length, ST_Envelope, ST_Area,
)
from sqlalchemy import select, text, RowMapping, func, Integer, String, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from configs.Database import get_db_connection
from models.BaseModel import AbstractMap
from models.maps import ZU
from schemas.archive import CreateQueryArchiveOpts
from schemas.map import CreateCommentOpts, FilterOpts
from services.archive import ArchiveService


class MapRepository:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db_connection),
        archive_service: ArchiveService = Depends(),
    ):
        self._db = db
        self._archive_service = archive_service

    async def create_comment(self, opts: CreateCommentOpts):
        query = select(ZU).filter(ZU.gid == opts.gid)

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        result = rows.scalars().first()
        if result:
            result.comments = opts.comment
            await result.commit()

    async def search_by_cadastra(self, cadastra: str) -> RowMapping:
        query = select(
            ZU.gid,
            ZU.cadastra2,
            ZU.address,
            ST_X(ST_Centroid(ZU.geom)).label("lon"),
            ST_Y(ST_Centroid(ZU.geom)).label("lat"),
            ZU.hasvalid5,
            ZU.hascadas6,
            ZU.isdraft,
            ZU.ownershi8,
            ZU.is_stroy,
            ZU.is_nonca20,
            ZU.area,
            ZU.comments,
            ST_AsGeoJSON(ZU.geom).label("geom"),
        ).filter(ZU.cadastra2 == cadastra)

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        result = rows.mappings().one()

        return result

    async def search_by_address(self, address: str) -> Sequence[RowMapping]:
        query = select(
            ZU.gid,
            ZU.cadastra2,
            ZU.address,
            ZU.hasvalid5,
            ZU.hascadas6,
            ZU.isdraft,
            ZU.ownershi8,
            ZU.is_stroy,
            ZU.is_nonca20,
            ZU.area,
            ZU.comments,
            ZU.address,
            ST_X(ST_Centroid(ZU.geom)).label("lon"),
            ST_Y(ST_Centroid(ZU.geom)).label("lat"),
            ZU.address_tsv,
            ST_AsGeoJSON(ZU.geom).label("geom"),
        ).filter(text(f"address_tsv @@ plainto_tsquery('russian', '{address}')"))

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        results = rows.mappings().all()

        return results

    async def get_map(self, class_map: AbstractMap) -> Sequence[RowMapping]:
        fields = [
            ST_AsGeoJSON(column).label("geom")
            if str(column) == f"{class_map.__tablename__}.geom"
            else column
            for column in class_map.__table__.columns
        ]

        fields.extend(
            [
                ST_X(ST_Centroid(class_map.geom)).label("lon"),
                ST_Y(ST_Centroid(class_map.geom)).label("lat"),
            ]
        )

        query = select(*fields)

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        result = rows.mappings().all()

        return result

    async def get_available_maps(self) -> Sequence[str]:
        rows = await self._db.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
        )

        result = rows.scalars().all()

        return result

    async def filters(
        self, model: AbstractMap, opts: FilterOpts
    ) -> Sequence[RowMapping]:
        fields = [
            ST_AsGeoJSON(column).label("geom")
            if str(column) == f"{model.__tablename__}.geom"
            else column
            for column in model.__table__.columns
        ]

        fields.extend(
            [
                ST_X(ST_Centroid(model.geom)).label("lon"),
                ST_Y(ST_Centroid(model.geom)).label("lat"),
            ]
        )

        query = select(*fields)

        for field, value in opts.filters.items():
            if hasattr(model, field):
                filter_value = value
                if isinstance(getattr(model, field).type, Integer):
                    filter_value = int(value)
                elif isinstance(getattr(model, field).type, String):
                    filter_value = str(value)
                elif isinstance(getattr(model, field).type, Numeric):
                    filter_value = float(value)

                query = query.filter(getattr(model, field) == filter_value)

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        results = rows.mappings().all()

        return results

    async def get_records_for_exporter(
        self, fields: List[str], model_class: AbstractMap, gids: List[int]
    ):
        query = select(*fields, model_class.geom).filter(model_class.gid.in_(gids))

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        results = rows.fetchall()

        return results

    async def maps_intersection(self, *models: AbstractMap):
        from_clause = models[0].__table__
        geom_aliases = [models[0].geom.label("valid_geom_0")]

        for i, model in enumerate(models[1:], start=1):
            valid_geom = model.geom.label(f"valid_geom_{i}")
            from_clause = from_clause.join(
                model,
                ST_Intersects(geom_aliases[-1], valid_geom) & ~ST_IsEmpty(valid_geom),
            )
            geom_aliases.append(valid_geom)

        intersection_geom = geom_aliases[0]
        for geom in geom_aliases[1:]:
            intersection_geom = ST_Intersection(intersection_geom, geom)

        query = (
            select(ST_AsGeoJSON(intersection_geom.label("geom_intersection")))
            .select_from(from_clause)
            .where(~ST_IsEmpty(intersection_geom))
        )

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        result = rows.scalars().all()

        return result

    async def get_dashboard(self):
        query = select(
            ZU.ownershi8,
            func.count(ZU.gid).label("count"),
            func.sum(ZU.area).label("total_area"),
        ).group_by(ZU.ownershi8)

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        results = rows.mappings().all()

        return results

    async def get_long_narrow_layers(
        self, class_map: AbstractMap, threshold_ratio: float
    ) -> Sequence[RowMapping]:
        fields = [
            ST_AsGeoJSON(column).label("geom")
            if str(column) == f"{class_map.__tablename__}.geom"
            else column
            for column in class_map.__table__.columns
        ]

        fields.extend(
            [
                ST_X(ST_Centroid(class_map.geom)).label("lon"),
                ST_Y(ST_Centroid(class_map.geom)).label("lat"),
            ]
        )

        query = select(*fields).filter(
            func.ST_Area(class_map.geom) > 0,
            (func.ST_XMax(func.ST_Envelope(class_map.geom)) - func.ST_XMin(func.ST_Envelope(class_map.geom))) /
            (func.ST_YMax(func.ST_Envelope(class_map.geom)) - func.ST_YMin(func.ST_Envelope(class_map.geom))) > threshold_ratio
        )

        start_time = time.monotonic()

        rows = await self._db.execute(query)

        elapsed_time = time.monotonic() - start_time

        await self._archive_service.create(
            CreateQueryArchiveOpts(text=str(query), elapsed_time=elapsed_time)
        )

        result = rows.mappings().all()

        return result
