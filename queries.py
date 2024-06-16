from sqlalchemy import select
from geoalchemy2.functions import (
    ST_Intersects,
    ST_AsGeoJSON,
    ST_Intersection,
    ST_IsEmpty,
)


def intersect_geoms(session, *models):
    """
    Returns the intersection of geometries from an arbitrary number of SQLAlchemy models using SQLAlchemy.

    :param session: SQLAlchemy session object.
    :param models: An arbitrary number of SQLAlchemy model classes.
    :return: A list of dictionaries representing the intersection of all the provided geometries.
    """

    # Initialize a variable to hold the intersection of all geometries
    from_clause = models[0].__table__
    geom_aliases = [models[0].geom.label("valid_geom_0")]

    for i, model in enumerate(models[1:], start=1):
        valid_geom = model.geom.label(f"valid_geom_{i}")
        from_clause = from_clause.join(
            model, ST_Intersects(geom_aliases[-1], valid_geom) & ~ST_IsEmpty(valid_geom)
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

    result = session.scalars(query).all()

    return result


# engine = create_engine(
#     "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = SessionLocal()
#
# class_maps = []
# mn_to_cl = map_name_to_class(schemas)
#
# maps = ["МКД", "район", "округ"]
#
# for map in maps:
#     class_maps.append(mn_to_cl[map])
#
# print(intersect_geoms(session, *class_maps))
