build:
	uv sync --active
	uv build --wheel --index pypi --out-dir build/

check:
	mypy test.py src/litesort/

test: build
	uv run test.py
