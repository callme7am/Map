from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.Database import get_db_connection
from models.archive import QueryArchive


class ArchiveRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_connection)):
        self._db = db

    async def create(self, opts: QueryArchive) -> None:
        self._db.add(opts)
        await self._db.commit()

    async def list(self) -> Sequence[QueryArchive]:
        query = select(QueryArchive).order_by(QueryArchive.timestamp.desc())

        rows = await self._db.execute(query)
        results = rows.scalars().all()

        return results
