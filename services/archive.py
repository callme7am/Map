from fastapi import Depends

from models.archive import QueryArchive
from repositories.archive import ArchiveRepository
from schemas.archive import CreateQueryArchiveOpts


class ArchiveService:
    def __init__(self, repository: ArchiveRepository = Depends()):
        self._repo = repository

    async def list(self):
        return await self._repo.list()

    async def create(self, opts: CreateQueryArchiveOpts) -> None:
        await self._repo.create(
            QueryArchive(query_text=opts.text, elapsed_time=opts.elapsed_time)
        )
