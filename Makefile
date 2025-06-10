# Makefile
.PHONY: install lint format test clean

install:
	pip install -r requirements.txt

lint:
	flake8 src tests

format:
	isort src tests && black src tests

test:
	pytest --cov=src --cov-report=term-missing

clean:
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov build dist *.egg-info
