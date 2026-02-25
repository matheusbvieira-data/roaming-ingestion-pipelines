# --- Global Variables ---
PYTHON := python3
PIP := pip
PROJECT_NAME := roaming-ingestion-pipelines

# --- Shell Commands ---
.DEFAULT_GOAL := help
.PHONY: help install format lint test clean fake

# --- 1. Help and Documentation ---
help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# --- 2. Local Development (Python) ---
install:  ## Installs project dependencies in editable mode
	python -m pip install --upgrade pip
	$(PIP) install -e .[dev]

format:  ## Formats code using Ruff
	ruff format .

lint:  ## Verifies style and bug issues using Ruff
	ruff check . --fix

test:  ## Runs unit and integration tests with Pytest
	pytest -v tests/ --cov=src --cov-report=term-missing --cov-report=html

# --- 3. Maintenance and cleaning ---
clean:  ## Cleans temp files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# --- 4. Generate fake data ---
fake:  ## Generates fake data for testing purposes
	python src/utils/fakedata.py
