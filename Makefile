init:
	pdm install

lint:
	pdm run ruff check src	
	pdm run ruff check tests
	pdm run codespell src	
	pdm run codespell tests

format:
	pdm run ruff format src
	pdm run ruff format tests

	pdm run ruff check src	
	pdm run ruff check tests

type:
	pdm run mypy src

test:
	pdm run pytest tests
