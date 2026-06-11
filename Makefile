.PHONY: install run debug clean lint lint-strict

MAIN := src.main
MAP := ?

install:
	uv sync

run:
	uv run python -m $(MAIN) $(MAP)

debug:
	uv run python -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	uv run flake8 . --exclude=.venv,__pycache__,.mypy_cache
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 . --exclude=.venv,__pycache__,.mypy_cache
	uv run mypy . --strict