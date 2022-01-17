THIS_FILE := $(lastword $(MAKEFILE_LIST))
SHELL := /bin/bash

.PHONY: help backend-collectstatic backend-compile-translations backend-install-dev backend-install backend-lint backend-lint-with-report backend-makemigrations backend-make-translations backend-migrate backend-test frontend-build frontend-build-dev frontend-install-dependencies frontend-lint-fix frontend-lint frontend-lint-with-report frontend-sasslint-fix frontend-sasslint frontend-sasslint-with-report frontend-test install-node-in-python-image install-yarn-in-python-image travis-after travis-before travis-install-dependencies travis-script

.DEFAULT: help

.EXPORT_ALL_VARIABLES:
NODE_VERSION = 16.x
YARN_VERSION = 1.13.0
PSQL_DBNAME = eventol
PSQL_PASSWORD = secret
PSQL_USER = eventol
PSQL_VERSION = 9.6
EXTERNAL_PORT = 80
PATH = $(shell printenv PATH):~/.yarn/bin:$(HOME)/.yarn/bin:$(HOME)/.config/yarn/global/node_modules/.bin

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

DOCKER_COMPOSE := cd deploy/docker && docker-compose
DOCKER_COMPOSE_PROD := $(DOCKER_COMPOSE) -f docker-compose.prod.yml

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
	mkdir -p eventol/static
	mkdir -p eventol/front/eventol/static
	cd eventol && python manage.py collectstatic --noinput

backend-createsuperuser: ## Run backend create super user
	cd eventol && python manage.py createsuperuser

backend-lint: ## Run backend linter
	pylint --output-format=colorized eventol/eventol eventol/manager

backend-lint-with-report: ## Run backend linter and generate report
	pylint --output-format=colorized --reports yes eventol/eventol eventol/manager

backend-make-translations: ## Update translations files (update .po files)
	cd eventol && python manage.py makemessages -a -d djangojs --no-location -i *.spec.jsx -i *.spec.js -i *.config.js -i bower_components -i node_modules -i venv -i coverage -e js,jsx
	cd eventol && python manage.py makemessages -a -d django --no-location -i bower_components -i node_modules -i venv -i coverage

backend-compile-translations: ## Compile translations files (update .mo files)
	cd eventol && python manage.py compilemessages

backend-runserver: ## Runserver for development environment
	cd eventol && python manage.py runserver 0.0.0.0:8000

## Frontend tasks
frontend-start-dev: ## Start frontend for development environment
	cd eventol/front && yarn start

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
	sudo apt remove -y nodejs
	curl -sL https://deb.nodesource.com/setup_$$NODE_VERSION | sudo bash -
	sudo apt install -y nodejs
	@$(MAKE) -f $(THIS_FILE) install-yarn-in-python-image

travis-script: frontend-install-dependencies frontend-build ## Travis script for run tests (python and react)
	mkdir -p eventol/static
	mkdir -p eventol/front/eventol/static
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

gitlab-autodeploy: ## Gitlab autodeploy command to remote server
	sshpass -e ssh -p$(SSH_PORT) -o stricthostkeychecking=no -x $(SSH_USER)@$(SSH_HOST) $(SSH_SCRIPT)

gitlab-registry-login: ## Gitlab login docker to registry
	docker login -u gitlab-ci-token -p $(CI_BUILD_TOKEN) $(CI_REGISTRY)

gitlab-build-and-push: ## Gitlab pull, build and push docker image
	docker pull $(IMAGE_NAME) || true
	docker build --cache-from $(IMAGE_NAME) -t $(IMAGE_NAME) .
	docker push $(IMAGE_NAME)

gitlab-update-image: gitlab-registry-login gitlab-build-and-push ## Gitlab update docker image in gitlab registry

# EventoL*
pull: ## Pull docker images for production environment
	$(DOCKER_COMPOSE_PROD) pull

pull-dev: ## Pull docker images for development environment
	$(DOCKER_COMPOSE) pull

status: ## Status for production environment
	$(DOCKER_COMPOSE_PROD) ps

status-dev: ## Status for development environment
	$(DOCKER_COMPOSE) ps

build-local: ## Build eventol latest image locally
	docker build --force-rm --tag=eventol/eventol:latest .

build: ## Build docker images for production environment
	$(DOCKER_COMPOSE_PROD) build --force-rm

build-dev: ## Build docker images for development environment
	$(DOCKER_COMPOSE) build --force-rm

deploy: pull build ## Deploy eventol with production environment
	$(DOCKER_COMPOSE_PROD) up -d --remove-orphans

deploy-dev: pull-dev build-dev ## Deploy eventol with development environment
	mkdir -p eventol/front/eventol
	mkdir -p deploy/docker/db/postgres
	touch eventol/front/webpack-stats-local.json
	$(DOCKER_COMPOSE) up -d --remove-orphans

logs: ## Show docker-compose logs of production environment
	$(DOCKER_COMPOSE_PROD) logs

logs-dev: ## Show docker-compose logs of development environment
	$(DOCKER_COMPOSE) logs

logs-follow: ## Show and follow docker-compose logs of production environment
	$(DOCKER_COMPOSE_PROD) logs -f

logs-follow-dev: ## Show and follow docker-compose logs of development environment
	$(DOCKER_COMPOSE) logs -f

restart: ## Restart eventol in production environment
	$(DOCKER_COMPOSE_PROD) restart

restart-dev: ## Restart eventol in development environment
	$(DOCKER_COMPOSE) restart

stop: ## Stop eventol in production environment
	$(DOCKER_COMPOSE_PROD) stop

stop-dev: ## Stop eventol in development environment
	$(DOCKER_COMPOSE) stop

undeploy: stop ## Remove eventol in production environment
	$(DOCKER_COMPOSE_PROD) down --remove-orphans

undeploy-dev: stop-dev ## Remove eventol in development environment
	$(DOCKER_COMPOSE) down --remove-orphans

undeploy-full: stop ## Remove eventol and data in production environment
	$(DOCKER_COMPOSE_PROD) down --remove-orphans --volumes

undeploy-full-dev: stop-dev ## Remove eventol and data in development environment
	$(DOCKER_COMPOSE) down --remove-orphans --volumes

update: undeploy deploy ## Update eventol in production environment
update-dev: undeploy-dev deploy-dev ## Update eventol in development environment

# EventoL commands from docker-compose
docker-backend-test: ## Run backend test with coverage in docker-compose
	$(DOCKER_COMPOSE) exec -T worker make backend-test

docker-backend-makemigrations: ## Run backend make migrations from manager app in docker-compose
	$(DOCKER_COMPOSE) exec -T worker make backend-makemigrations

docker-backend-migrate: ## Run backend migrate database in docker-compose
	$(DOCKER_COMPOSE_PROD) exec -T worker make backend-migrate

docker-backend-collectstatic: ## Run backend collect static files in docker-compose
	mkdir -p eventol/static
	mkdir -p eventol/front/eventol/static
	$(DOCKER_COMPOSE_PROD) exec -T worker make backend-collectstatic

docker-backend-createsuperuser: ## Run backend create super user in docker-compose
	$(DOCKER_COMPOSE_PROD) exec -T worker make backend-createsuperuser

docker-backend-lint: ## Run backend linter in docker-compose
	$(DOCKER_COMPOSE) exec -T worker make backend-lint

docker-backend-lint-with-report: ## Run backend linter and generate report in docker-compose
	$(DOCKER_COMPOSE) exec -T worker make backend-lint-with-report

docker-backend-make-translations: ## Update translations files (update .po files) in docker-compose
	$(DOCKER_COMPOSE) exec -T worker make backend-make-translations

docker-backend-compile-translations: ## Compile translations files (update .mo files) in docker-compose
	$(DOCKER_COMPOSE_PROD) exec -T worker make backend-compile-translations

docker-backend-runserver: ## Runserver for development environment in docker-compose
	$(DOCKER_COMPOSE_PROD) exec -T worker make backend-runserver

docker-frontend-start-dev: ## Start frontend for development environment in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn start

docker-frontend-install-dependencies: ## Install frontend dev dependencies in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn install

docker-frontend-build: ## Build frontend code for production environment in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn build

docker-frontend-build-dev: ## Build frontend code for development environment in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn yarn build:dev

docker-frontend-test: ## Run frontend test in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn test

docker-frontend-lint: ## Run frontend linter in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn eslint

docker-frontend-lint-fix: ## Run frontend linter and autofix errors in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn eslint:fix

docker-frontend-lint-with-report: ## Run frontend linter and generate report in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn eslint:report

docker-frontend-sasslint: ## Run sass linter in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn sasslint

docker-frontend-sasslint-fix: ## Run sass linter and autofix errors in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn sasslint:fix

docker-frontend-sasslint-with-report: ## Run sass linter and generate report in docker-compose
	$(DOCKER_COMPOSE) exec -T reactjs yarn sasslint:report

## Alias
collectstatic: docker-backend-collectstatic ## Alias to docker-backend-collectstatic
createsuperuser: docker-backend-createsuperuser ## Alias to docker-backend-createsuperuser
makemigrations: docker-backend-makemigrations ## Alias to docker-backend-makemigrations
migrate: docker-backend-migrate ## Alias to docker-backend-migrate
runserver: docker-backend-runserver ## Alias to docker-backend-runserver
setup-frontend: docker-frontend-install-dependencies ## Setup front end in docker-compose
start-frontend: docker-frontend-start-dev ## Alias to docker-frontend-start-dev
make-translations: docker-backend-make-translations ## Alias to docker-backend-make-translations
compile-translations: docker-backend-compile-translations ## Alias to docker-backend-compile-translations
