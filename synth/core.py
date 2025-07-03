import logging
import random
from collections import defaultdict, deque

from faker import Faker
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    Numeric,
    String,
    Text,
    create_engine,
)

_faker = Faker()


def generate_value(column: Column) -> str:
    """
    Return a SQL-literal string for a synthetic value in this column.
    """
    col_type = column.type

    # Integer types
    if isinstance(col_type, Integer):
        return str(_faker.random_int(min=0, max=10000))

    # Decimal / Numeric
    if isinstance(col_type, Numeric):
        # Adjust digits as needed
        dec = _faker.pydecimal(left_digits=5, right_digits=2, positive=True)
        return str(dec)

    # Boolean
    if isinstance(col_type, Boolean):
        return 'TRUE' if _faker.boolean() else 'FALSE'

    # Date/time
    if isinstance(col_type, DateTime):
        dt = _faker.date_time().isoformat(sep=' ')
        return f"'{dt}'"

    # String / Text
    if isinstance(col_type, (String, Text)):
        max_len = getattr(col_type, 'length', 50) or 50
        text = _faker.text(max_nb_chars=max_len)
        # Escape single quotes for SQL
        safe = text.replace("'", "''")
        return f"'{safe}'"

    # Fallback to a single word
    return f"'{_faker.word()}'"


def generate_dump(
    db_url: str, rows: int, seed: int | None, out_file: str, verbose: bool
):
    """
    Connects to the given DB URL, reflects schema, orders tables,
    and (eventually) generates a synthetic SQL dump.
    """
    # 1. Configure logging
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

    # 2. Seed the RNG (if provided)
    if seed is not None:
        random.seed(seed)
        logging.info(f'Random seed set to {seed}')

    # 3. Reflect schema
    logging.info(f'Reflecting schema from {db_url!r}')
    metadata = reflect_schema(db_url)
    table_names = list(metadata.tables.keys())
    logging.info(f'Discovered tables: {table_names}')

    # 4. Compute insertion order
    try:
        order = compute_table_order(metadata)
        logging.info(f'Table insertion order: {order}')
        for tbl_name in order:
            table = metadata.tables[tbl_name]
            # generate a single sample row’s values
            vals = [generate_value(col) for col in table.columns]
            cols = [col.name for col in table.columns]
            logging.info(
                'Sample INSERT for %s: INSERT INTO %s (%s) VALUES (%s);',
                tbl_name,
                tbl_name,
                ', '.join(cols),
                ', '.join(vals),
            )
    except ValueError as e:
        logging.error(str(e))
        raise

    # 5. TODO: Generate data & write to out_file
    logging.info(f'(stub) Would generate {rows} rows per table into {out_file!r}')
    # e.g. with open(out_file, "w") as f: f.write("-- SQL DUMP HERE\n")

    # Example stub return
    return order


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
