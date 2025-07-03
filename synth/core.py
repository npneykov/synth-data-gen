import logging
from collections import defaultdict, deque

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


def compute_table_order(metadata: MetaData) -> list[str]:
    """
    Return a list of table names in an order that respects foreign-key
    dependencies (parents before children), using Kahn’s topological sort.
    """
    # Build dependency map: table → set of tables it depends on
    deps: dict[str, set[str]] = defaultdict(set)
    for tbl in metadata.tables.values():
        deps.setdefault(tbl.name, set())
        for fk in tbl.foreign_keys:
            deps[tbl.name].add(fk.column.table.name)

    # Initialize queue with tables that have no dependencies
    ready = deque([name for name, d in deps.items() if not d])
    order: list[str] = []

    while ready:
        tbl_name = ready.popleft()
        order.append(tbl_name)

        # Remove this table from others’ dependency sets
        for other, dset in deps.items():
            if tbl_name in dset:
                dset.remove(tbl_name)
                if not dset:
                    ready.append(other)

    # If we didn’t sort all tables, there’s a cycle
    if len(order) != len(deps):
        cycle = set(deps.keys()) - set(order)
        raise ValueError(f'Circular foreign-key dependency detected: {cycle!r}')

    return order
