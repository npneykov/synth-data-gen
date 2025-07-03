import pytest
from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, create_engine

from synth.core import compute_table_order, reflect_schema


def test_linear_fk_chain(tmp_path):
    """Simple parent → child chain should sort correctly."""
    url = f"sqlite:///{tmp_path / 'chain.db'}"
    eng = create_engine(url)
    md = MetaData()

    parent = Table('parent', md, Column('id', Integer, primary_key=True))
    child = Table(
        'child',
        md,
        Column('id', Integer, primary_key=True),
        Column('parent_id', Integer, ForeignKey('parent.id')),
    )
    md.create_all(eng)

    metadata = reflect_schema(url)
    order = compute_table_order(metadata)
    assert order.index('parent') < order.index('child')


def test_cycle_detection(tmp_path):
    """A → B → A should raise a ValueError for the cycle."""
    url = f"sqlite:///{tmp_path / 'cycle.db'}"
    eng = create_engine(url)
    md = MetaData()

    a = Table(
        'a',
        md,
        Column('id', Integer, primary_key=True),
        Column('b_id', Integer, ForeignKey('b.id')),
    )
    b = Table(
        'b',
        md,
        Column('id', Integer, primary_key=True),
        Column('a_id', Integer, ForeignKey('a.id')),
    )

    md.create_all(eng)

    metadata = reflect_schema(url)
    with pytest.raises(ValueError) as exc:
        compute_table_order(metadata)
    assert 'Circular foreign-key dependency' in str(exc.value)
