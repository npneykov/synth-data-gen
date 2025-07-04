PY := python
PIP := $(PY) -m pip
VENV := .venv

.PHONY: init lint format test build clean

init:
	$(PY) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	$(PY) -m pre-commit install

lint:
	$(PY) -m ruff check .
	$(PY) -m black --check --diff .

format:
	$(PY) -m black .
	$(PY) -m ruff format .

test:
	$(PY) -m pytest -q

build:
	PYTHONPATH=. \
	python -m PyInstaller synth/cli.py \
	--onefile \
	--name synthgen \
	--add-data "legal/EULA_v1.0.txt:."

clean:
	$(PY) - <<'PY'
	import shutil, pathlib, sys, os
	for d in ("build","dist","__pycache__",".pytest_cache"):
	shutil.rmtree(d, ignore_errors=True)
	PY
