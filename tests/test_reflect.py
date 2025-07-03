import pytest
from sqlalchemy import Column, Integer, MetaData, Table, create_engine

from synth.core import reflect_schema


def test_reflect(tmp_path):
    db_file = tmp_path / 'test.db'
    url = f'sqlite:///{db_file}'
    # Create a simple SQLite schema
    engine = create_engine(url)
    metadata = MetaData()
    Table('users', metadata, Column('id', Integer, primary_key=True))
    metadata.create_all(engine)

    # Reflect the schema
    reflected = reflect_schema(url)
    assert 'users' in reflected.tables
    # Column count matches
    cols = reflected.tables['users'].columns
    assert 'id' in cols
