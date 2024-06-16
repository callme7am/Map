from datetime import datetime

from sqlalchemy import Integer, Column, Text, Date, Float

from models.BaseModel import EntityMeta


class QueryArchive(EntityMeta):
    __tablename__ = "query_archive"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    timestamp = Column(Date, default=datetime.now)
    elapsed_time = Column(Float, nullable=False)

