from abc import ABCMeta, ABC, abstractmethod

from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

EntityMeta = declarative_base()


class AbstractMapMeta(ABCMeta, DeclarativeMeta):
    pass


class AbstractMap(ABC, EntityMeta, metaclass=AbstractMapMeta):
    __abstract__ = True

    geom = Column(Geometry("MULTIPOLYGON", srid=4326))

    @staticmethod
    @abstractmethod
    def get_popup(row): ...
