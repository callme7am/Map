import inspect

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from schemas import Base
from sqlalchemy.inspection import inspect as sqinspect


def get_session(database_url):
    engine = create_engine(database_url)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def get_all_table_names(session):
    result = session.execute(
        text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
    )

    return result.scalars().all()


def map_name_to_class(module):
    classes = {}

    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if inspect.isclass(attribute):
            # Add the class to the list if it is defined in the module
            if attribute.__module__ == module.__name__ and hasattr(
                attribute, "__tablename__"
            ):
                classes[attribute.__tablename__] = attribute
    return classes


def object_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in sqinspect(obj).mapper.column_attrs}
