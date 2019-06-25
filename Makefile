THIS_FILE := $(lastword $(MAKEFILE_LIST))
SHELL := /bin/bash

.PHONY: help backend-collectstatic backend-compile-translations backend-install-dev backend-install backend-lint backend-lint-with-report backend-makemigrations backend-make-translations backend-migrate backend-test frontend-build frontend-build-dev frontend-install-dependencies frontend-lint-fix frontend-lint frontend-lint-with-report frontend-sasslint-fix frontend-sasslint frontend-sasslint-with-report frontend-test install-node-in-python-image install-yarn-in-python-image travis-after travis-before travis-install-dependencies travis-script

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

## Install dependencies
install-node-in-python-image: ## Install node in python image
	curl -sL https://deb.nodesource.com/setup_$$NODE_VERSION | bash -
	apt install -y nodejs

install-yarn-in-python-image: ## Install yarn and node in python image if node is not installed
	if which node > /dev/null; then \
		node -v; \
		echo "node is installed, skipping..."; \
	else \
		curl -sL https://deb.nodesource.com/setup_$$NODE_VERSION | bash -; \
		apt install -y nodejs; \
	fi
	curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version $$YARN_VERSION

## Backend tasks
backend-install: ## Install python production dependencies
	pip install -U pip wheel
	pip install -r requirements.txt

backend-install-dev: backend-install ## Install python development dependencies
	pip install -r requirements-dev.txt

backend-test: ## Run backend test with coverage
	cd eventol && py.test --cov-report xml --cov-report term-missing --cov-report html --cov --cov-branch -n auto

backend-makemigrations: ## Run backend make migrations from manager app
	cd eventol && python manage.py makemigrations manager

backend-migrate: ## Run backend migrate database
	cd eventol && python manage.py migrate

backend-collectstatic: ## Run backend collect static files
	cd eventol && python manage.py collectstatic --noinput

backend-lint: ## Run backend linter
	pylint --output-format=colorized eventol/eventol eventol/manager

backend-lint-with-report: ## Run backend linter and generate report
	pylint --output-format=colorized --reports yes eventol/eventol eventol/manager

backend-make-translations: ## Update translations files (update .po files)
	cd eventol && python manage.py makemessages -a -d djangojs --no-location -i node_modules -i venv -i bower_components -i coverage -e js,jsx
	cd eventol && python manage.py makemessages -a -d django --no-location -i node_modules -i venv -i bower_components -i coverage

backend-compile-translations: ## Compile translations files (update .mo files)
	cd eventol && python manage.py compilemessages

## Frontend tasks
frontend-install-dependencies: ## Install frontend dev dependencies
	cd eventol/front && yarn install

frontend-build: ## Build frontend code for production environment
	cd eventol/front && yarn build

frontend-build-dev: ## Build frontend code for development environment
	cd eventol/front && yarn build:dev

frontend-test: ## Run frontend test
	cd eventol/front && yarn test

frontend-lint: ## Run frontend linter
	cd eventol/front && yarn eslint

frontend-lint-fix: ## Run frontend linter and autofix errors
	cd eventol/front && yarn eslint:fix

frontend-lint-with-report: ## Run frontend linter and generate report
	cd eventol/front && yarn eslint:report

frontend-sasslint: ## Run sass linter
	cd eventol/front && yarn sasslint

frontend-sasslint-fix: ## Run sass linter and autofix errors
	cd eventol/front && yarn sasslint:fix

frontend-sasslint-with-report: ## Run sass linter and generate report
	cd eventol/front && yarn sasslint:report

## Travis CI
travis-install-dependencies: ## Install coverage and coveralls dependencies
	pip install coverage coveralls

travis-before: ## Travis before commands
	docker run --name eventol-postgres -e POSTGRES_PASSWORD=$$PSQL_PASSWORD -e POSTGRES_USER=$$PSQL_USER -e POSTGRES_DB=$$PSQL_DBNAME -p $$PSQL_PORT:5432 -d postgres:$$PSQL_VERSION
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	./cc-test-reporter before-build
	@$(MAKE) -f $(THIS_FILE) install-yarn-in-python-image

travis-script: frontend-install-dependencies frontend-build ## Travis script for run tests (python and react)
	mkdir -p eventol/static
	@$(MAKE) -f $(THIS_FILE) backend-makemigrations
	@$(MAKE) -f $(THIS_FILE) backend-migrate
	@$(MAKE) -f $(THIS_FILE) backend-collectstatic
	@$(MAKE) -f $(THIS_FILE) backend-test
	@$(MAKE) -f $(THIS_FILE) frontend-test

travis-after: ## Travis after script for success case
	cd eventol && coverage report
	cd eventol && coveralls
	mv cc-test-reporter eventol/cc-test-reporter 
	cd eventol && ./cc-test-reporter format-coverage -d -t coverage.py -o coverage/python.json --add-prefix eventol
	cd eventol && ./cc-test-reporter format-coverage ./front/coverage/lcov.info -d -t lcov -o ./coverage/javascript.json --add-prefix eventol
	cd eventol && ./cc-test-reporter sum-coverage --output coverage/codeclimate.json -d -p 2 coverage/python.json coverage/javascript.json
	cd eventol && ./cc-test-reporter upload-coverage -d

## Gitlab
gitlab-python-testing: install-yarn-in-python-image frontend-install-dependencies frontend-build backend-install-dev backend-test ## Gitlab command for python-testing job
gitlab-python-lint: backend-install-dev backend-lint-with-report ## Gitlab command for python-lint job
gitlab-react-testing: frontend-install-dependencies frontend-test ## Gitlab command for react-testing job
gitlab-react-lint: frontend-install-dependencies frontend-lint ## Gitlab command for react-lint job
gitlab-react-lint-with-report: frontend-install-dependencies frontend-lint-with-report ## Gitlab command for react-lint-report job
gitlab-react-sasslint: frontend-install-dependencies frontend-sasslint ## Gitlab command for react-sasslint job
gitlab-react-sasslint-with-report: frontend-install-dependencies frontend-sasslint-with-report ## Gitlab command for react-sasslint-report job
