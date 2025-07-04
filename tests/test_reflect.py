from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, MetaData, Table, create_engine

from synth.core import reflect_schema


@pytest.fixture(scope='module')
def project_db_url():
    root = Path(__file__).parent.parent
    db_dir = root / 'test_db'
    db_dir.mkdir(exist_ok=True)
    return db_dir


def test_reflect(project_db_url):
    db_file = project_db_url / 'test.db'
    url = f'sqlite:///{db_file}'

    engine = create_engine(url)
    metadata = MetaData()
    Table('u', metadata, Column('id', Integer, primary_key=True))
    metadata.create_all(engine)

    # Run your reflection
    metadata = reflect_schema(url)
    assert 'u' in metadata.tables
