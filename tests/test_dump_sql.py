import os

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

from synth.core import generate_dump


def test_dump_sql(tmp_path):
    # Create a simple schema
    db_file = tmp_path / 'test.db'
    url = f'sqlite:///{db_file}'
    engine = create_engine(url)
    metadata = MetaData()
    Table(
        'u',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
    )
    metadata.create_all(engine)

    # Run dump
    out_file = tmp_path / 'dump.sql'
    order = generate_dump(
        str(url), rows=10, seed=None, out_file=str(out_file), verbose=False
    )

    # Verify file exists
    assert os.path.exists(out_file)
    lines = out_file.read_text().splitlines()
    assert 'BEGIN;' in lines
    assert 'COMMIT;' in lines

    # Exactly 3 INSERTs for our table
    inserts = [line for line in lines if line.startswith('INSERT INTO u')]
    assert len(inserts) == 10

    # The function should return the insertion order
    assert order == ['u']
