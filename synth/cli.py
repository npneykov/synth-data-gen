#!/usr/bin/env python3
# synth/cli.py

import typer

from synth import core

app = typer.Typer(
    name='synthgen',
    help='Synthetic Test-Data Generator — produce realistic, FK-aware SQL dumps.',
)


@app.command()
def generate(
    db: str = typer.Option(
        ...,
        '--db',
        '-d',
        help='SQLAlchemy database URL for the source schema (read-only).',
    ),
    rows: int = typer.Option(
        1000, '--rows', '-r', help='Approximate number of rows per table.'
    ),
    seed: int = typer.Option(
        42, '--seed', '-s', help='Random seed for reproducibility.'
    ),
    out_file: str = typer.Option(
        'dumpl.sql',
        '--out',
        '-o',
        help='Path to write the generated SQL dump file ( use `-` for stdout).',
    ),
    verbose: bool = typer.Option(
        False, '--verbose', '-v', help='Enable verbose output.'
    ),
):
    """
    Connects to the given database URL, reflects its schema, and emits
    a synthetic SQL dump respecting foreign keys and number of rows.
    """
    core.generate_dump(
        db_url=db,
        rows=rows,
        seed=seed,
        out_file=out_file,
        verbose=verbose,
    )


if __name__ == '__main__':
    app()
