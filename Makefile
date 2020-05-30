
LENGTH=120

.PHONY: format
format: black isort

.PHONY: pylint
pylint:
	pylint src tests --reports=n --max-line-length=$(LENGTH) --output-format=text

.PHONY: isort
isort:
	@echo -n "Run isort"
	isort --lines $(LENGTH) -rc src tests

.PHONY: black
black:
	@echo -n "Run black"
	black -l $(LENGTH) src tests

.PHONY: check-isort
check-isort:
	isort --lines $(LENGTH) -vb -rc --check-only -df src tests

.PHONY: check-styles
check-styles:
	pycodestyle src tests --max-line-length=$(LENGTH) --format pylint --exclude=migrations --ignore=E203,W503

.PHONY: check-black
check-black:
	black --check --diff -v -l $(LENGTH) src tests

.PHONY: checks
checks: check-styles check-isort check-black pylint tests

.PHONY: tests
tests:
	pytest -v --cov=src -v --cov-report=xml --cov-report=term

.PHONY: update-requirements
update-requirements:
	pip-compile -U --generate-hashes --output-file requirements/main.txt requirements/main.in
	pip-compile -U --generate-hashes --output-file requirements/dev.txt requirements/dev.in

.PHONY: install-requirements
install-requirements:
	pip install -r requirements/main.txt -U
	pip install -r requirements/dev.txt



