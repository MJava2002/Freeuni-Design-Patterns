.PHONY: help
.DEFAULT_GOAL := help

help:
	python -m library --help

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort core infra runner tests
	black core infra runner tests

lint: ## Run code linters
	isort --check core infra runner tests
	black --check core infra runner tests
	flake8 core infra runner tests
	mypy core infra runner tests

test:  ## Run tests with coverage
	pytest --cov
