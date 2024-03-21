.PHONY: help
.DEFAULT_GOAL := help

help:
	python -m app --help

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort pos tests
	black pos tests

lint: ## Run code linters
	isort --check pos tests
	black --check pos tests
	flake8 pos tests
	mypy pos tests

test:  ## Run tests with coverage
	pytest --cov
