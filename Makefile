THIS_FILE := $(lastword $(MAKEFILE_LIST))
SHELL := /bin/bash

.PHONY: help backend-collectstatic backend-compile-translations backend-install-dev backend-install backend-lint backend-lint-with-report backend-makemigrations backend-make-translations backend-migrate backend-test
.DEFAULT: help

.EXPORT_ALL_VARIABLES:
PSQL_DBNAME = eventol
PSQL_PASSWORD = secret
PSQL_USER = eventol
PSQL_VERSION = 9.6
EXTERNAL_PORT = 80
PATH = $(shell printenv PATH)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

DOCKER_COMPOSE := cd deploy/docker && docker compose
DOCKER_COMPOSE_PROD := $(DOCKER_COMPOSE) -f docker-compose.yml

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
	ruff check eventol/eventol eventol/manager
	ruff format --check eventol/eventol eventol/manager
	pylint --output-format=colorized eventol/eventol eventol/manager

backend-lint-with-report: ## Run backend linter and generate report
	ruff check eventol/eventol eventol/manager
	ruff format --check eventol/eventol eventol/manager
	pylint --output-format=colorized --reports yes eventol/eventol eventol/manager

backend-make-translations: ## Update translations files (update .po files)
	cd eventol && python manage.py makemessages -a -d djangojs --no-location -i *.spec.jsx -i *.spec.js -i *.config.js -i bower_components -i node_modules -i venv -i coverage -e js,jsx
	cd eventol && python manage.py makemessages -a -d django --no-location -i bower_components -i node_modules -i venv -i coverage

backend-compile-translations: ## Compile translations files (update .mo files)
	cd eventol && python manage.py compilemessages

backend-runserver: ## Runserver for development environment
	cd eventol && python manage.py runserver 0.0.0.0:8000

## Gitlab
gitlab-python-testing: backend-install-dev backend-test ## Gitlab command for python-testing job
gitlab-python-lint: backend-install-dev backend-lint-with-report ## Gitlab command for python-lint job

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

## Alias
collectstatic: docker-backend-collectstatic ## Alias to docker-backend-collectstatic
createsuperuser: docker-backend-createsuperuser ## Alias to docker-backend-createsuperuser
makemigrations: docker-backend-makemigrations ## Alias to docker-backend-makemigrations
migrate: docker-backend-migrate ## Alias to docker-backend-migrate
runserver: docker-backend-runserver ## Alias to docker-backend-runserver
make-translations: docker-backend-make-translations ## Alias to docker-backend-make-translations
compile-translations: docker-backend-compile-translations ## Alias to docker-backend-compile-translations
