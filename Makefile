init:
	pdm install

lint:
	pdm run ruff check src	
	pdm run ruff check tests
	pdm run codespell src	
	pdm run codespell tests
	pdm run codespell README.md

format:
	pdm run ruff format src
	pdm run ruff format tests

	pdm run ruff check src	
	pdm run ruff check tests

type:
	pdm run mypy src

test:
	pdm run pytest tests
