import logging

from sqlalchemy import MetaData, create_engine


def generate_dump(db_url, rows, seed, out_file, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)
    logging.info('Reflecting schema from %s', db_url)
    metadata = reflect_schema(db_url)
    logging.info('Found tables: %s', list(metadata.tables.keys()))
    # TODO: generate data…


def reflect_schema(db_url: str) -> MetaData:
    """
    Connects to db_url, reflects all tables, and FK relationships,
    and returns a populated MetaData object.
    """
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata
