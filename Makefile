THIS_FILE := $(lastword $(MAKEFILE_LIST))
SHELL := /bin/bash

.PHONY: help travis-ci gitlab

.DEFAULT: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

travis-before: ## Travis before commands
	docker run --name eventol-postgres -e POSTGRES_PASSWORD=$$PSQL_PASSWORD -e POSTGRES_USER=$$PSQL_USER -e POSTGRES_DB=$$PSQL_DBNAME -p $$PSQL_PORT:5432 -d postgres:$$PSQL_VERSION
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	./cc-test-reporter before-build 
	curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version $$YARN_VERSION
	export PATH=$$HOME/.yarn/bin:$$PATH

travis-install: ## Travis install before script
	pip install -U pip wheel
	pip install coverage coveralls
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

travis-script: ## Travis script for run tests (python and react)
	cd eventol/front
	yarn install
	yarn build
	cd -
	mkdir -p eventol/static
	cd eventol
	python manage.py makemigrations manager
	python manage.py migrate
	python manage.py collectstatic --noinput
	py.test --cov-report xml --cov-report term-missing --cov-report html --cov --cov-branch
	cd -
	cd eventol/front
	yarn install
	yarn test
	cd -

travis-after: ## Travis after script for success case
	cd eventol
	coverage report
	coveralls
	cd -
	mv cc-test-reporter eventol/cc-test-reporter 
	cd eventol
	./cc-test-reporter format-coverage -d -t coverage.py -o coverage/python.json --add-prefix eventol
	./cc-test-reporter format-coverage ./front/coverage/lcov.info -d -t lcov -o ./coverage/javascript.json --add-prefix eventol
	./cc-test-reporter sum-coverage --output coverage/codeclimate.json -d -p 2 coverage/python.json coverage/javascript.json
	./cc-test-reporter upload-coverage -d
	

