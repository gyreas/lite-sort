TESTDIR := ".testdir"

build:
	uv sync --active
	uv build --wheel --index pypi --out-dir build/

check:
	mypy test.py src/litesort/

test testdir=TESTDIR:
	TESTDIR={{testdir}} pytest --basetemp={{testdir}} test.py
