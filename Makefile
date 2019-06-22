THIS_FILE := $(lastword $(MAKEFILE_LIST))
SHELL := /bin/bash

.PHONY: help travis-ci gitlab

.DEFAULT: help

.EXPORT_ALL_VARIABLES:
NODE_VERSION = 10.x
YARN_VERSION = 1.13.0
PSQL_DBNAME = eventol
PSQL_PASSWORD = secret
PSQL_USER = eventol
PSQL_VERSION = 9.6
PATH = $(shell printenv PATH):~/.yarn/bin:$(HOME)/.yarn/bin:$(HOME)/.config/yarn/global/node_modules/.bin


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

python-image-install-node: ## Install node in python image
	curl -sL https://deb.nodesource.com/setup_$$NODE_VERSION | sudo bash -
	sudo apt install -y nodejs
	nvm use 10

python-image-install-yarn: ## Install yarn and node in python image if node is not installed
	if which node > /dev/null; then \
		node -v; \
		echo "node is installed, skipping..."; \
	else \
		curl -sL https://deb.nodesource.com/setup_$$NODE_VERSION | bash -; \
		apt install -y nodejs; \
	fi
	curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version $$YARN_VERSION

install-js-dependencies: ## Install dev dependencies
	cd eventol/front && yarn install

build-js: ## Build js code for production environment
	cd eventol/front && yarn build

travis-before: ## Travis before commands
	docker run --name eventol-postgres -e POSTGRES_PASSWORD=$$PSQL_PASSWORD -e POSTGRES_USER=$$PSQL_USER -e POSTGRES_DB=$$PSQL_DBNAME -p $$PSQL_PORT:5432 -d postgres:$$PSQL_VERSION
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	./cc-test-reporter before-build
	node -v;
	@$(MAKE) -f $(THIS_FILE) python-image-install-node
	@$(MAKE) -f $(THIS_FILE) python-image-install-yarn

python-install-dev: ## Python install dev dependencies
	pip install -U pip wheel
	pip install coverage coveralls
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

python-test: ## Python run test with coverage
	cd eventol && py.test --cov-report xml --cov-report term-missing --cov-report html --cov --cov-branch

travis-script: install-js-dependencies build-js ## Travis script for run tests (python and react)
	mkdir -p eventol/static
	cd eventol && python manage.py makemigrations manager
	cd eventol && python manage.py migrate
	cd eventol && python manage.py collectstatic --noinput
	@$(MAKE) -f $(THIS_FILE) python-test
	cd eventol/front && yarn install
	cd eventol/front && yarn test

travis-after: ## Travis after script for success case
	cd eventol && coverage report
	cd eventol && coveralls
	mv cc-test-reporter eventol/cc-test-reporter 
	cd eventol && ./cc-test-reporter format-coverage -d -t coverage.py -o coverage/python.json --add-prefix eventol
	cd eventol && ./cc-test-reporter format-coverage ./front/coverage/lcov.info -d -t lcov -o ./coverage/javascript.json --add-prefix eventol
	cd eventol && ./cc-test-reporter sum-coverage --output coverage/codeclimate.json -d -p 2 coverage/python.json coverage/javascript.json
	cd eventol && ./cc-test-reporter upload-coverage -d
	

