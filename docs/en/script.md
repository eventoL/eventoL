# Test script

To facilitate EventoL commands (for production and development), we create a *Makefile*

## Help

```bash
make help
```

## Available tasks

### Backend

- **backend-runserver**: Runserver for development environment
- **backend-install**: Install python production dependencies
- **backend-install-dev**: Install python development dependencies
- **backend-lint**: Run backend linter
- **backend-lint-with-report**: Run backend linter and generate report
- **backend-makemigrations**: Run backend make migrations from manager app
- **backend-migrate**: Run backend migrate database
- **backend-collectstatic**: Run backend collect static files
- **backend-make-translations**: Update translations files (update .po files)
- **backend-compile-translations**: Compile translations files (update .mo files)
- **backend-test**: Run backend test with coverage

### Frontend

- **frontend-start-dev**: Start frontend for development environment
- **frontend-build**: Build frontend code for production environment
- **frontend-build-dev**: Build frontend code for development environment
- **frontend-install-dependencies**: Install frontend dev dependencies
- **frontend-lint**: Run frontend linter
- **frontend-lint-fix**: Run frontend linter and autofix errors
- **frontend-lint-with-report**: Run frontend linter and generate report
- **frontend-sasslint**: Run sass linter
- **frontend-sasslint-fix**: Run sass linter and autofix errors
- **frontend-sasslint-with-report**: Run sass linter and generate report
- **frontend-test**: Run frontend test

### Docker

- **pull**: Pull docker images for production environment
- **pull-dev**: Pull docker images for development environment
- **build**: Build docker images for production environment
- **build-dev**: Build docker images for development environment
- **deploy**: Deploy eventol with production environment
- **deploy-dev**: Deploy eventol with development environment
- **restart**: Restart eventol in production environment
- **restart-dev**: Restart eventol in development environment
- **update**: Update eventol in production environment
- **update-dev**: Update eventol in development environment
- **logs**: Show docker-compose logs of production environment
- **logs-dev**: Show docker-compose logs of development environment
- **logs-follow**: Show and follow docker-compose logs of production environment
- **logs-follow-dev**: Show and follow docker-compose logs of development environment
- **status**: Status for production environment
- **status-dev**: Status for development environment
- **stop**: Stop eventol in production environment
- **stop-dev**: Stop eventol in development environment
- **undeploy**: Remove eventol in production environment
- **undeploy-dev**: Remove eventol in development environment
- **undeploy-full**: Remove eventol and data in production environment
- **undeploy-full-dev**: Remove eventol and data in development environment
  
### Backend and frontend commands with docker-compose

- **docker-backend-collectstatic**: Run backend collect static files in docker-compose
- **docker-backend-compile-translations**: Compile translations files (update .mo files) in docker-compose
- **docker-backend-lint**: Run backend linter in docker-compose
- **docker-backend-lint-with-report**: Run backend linter and generate report in docker-compose
- **docker-backend-makemigrations**: Run backend make migrations from manager app in docker-compose
- **docker-backend-make-translations**: Update translations files (update .po files) in docker-compose
- **docker-backend-migrate**: Run backend migrate database in docker-compose
- **docker-backend-runserver**: Runserver for development environment in docker-compose
- **docker-backend-test**: Run backend test with coverage in docker-compose
- **docker-frontend-build**: Build frontend code for production environment in docker-compose
- **docker-frontend-build-dev**: Build frontend code for development environment in docker-compose
- **docker-frontend-install-depend**: ncies Install frontend dev dependencies in docker-compose
- **docker-frontend-lint-fix**: Run frontend linter and autofix errors in docker-compose
- **docker-frontend-lint**: Run frontend linter in docker-compose
- **docker-frontend-lint-with-report**: Run frontend linter and generate report in docker-compose
- **docker-frontend-sasslint-fix**: Run sass linter and autofix errors in docker-compose
- **docker-frontend-sasslint**: Run sass linter in docker-compose
- **docker-frontend-sasslint-with-report**: Run sass linter and generate report in docker-compose
- **docker-frontend-start-dev**: Start frontend for development environment in docker-compose
- **docker-frontend-test**: Run frontend test in docker-compose

### Gitlab ci/cd

- **gitlab-autodeploy**: Gitlab autodeploy command to remote server
- **gitlab-build-and-push**: Gitlab pull, build and push docker image
- **gitlab-python-lint**: Gitlab command for python-lint job
- **gitlab-python-testing**: Gitlab command for python-testing job
- **gitlab-react-lint**: Gitlab command for react-lint job
- **gitlab-react-lint-with-report**: Gitlab command for react-lint-report job
- **gitlab-react-sasslint**: Gitlab command for react-sasslint job
- **gitlab-react-sasslint-with-report**: Gitlab command for react-sasslint-report job
- **gitlab-react-testing**: Gitlab command for react-testing job
- **gitlab-registry-login**: Gitlab login docker to registry
- **gitlab-update-image**: Gitlab update docker image in gitlab registry

## Run one task

```bash
make TASK_NAME
```

## Run two or more tasks

```bash
make TASK_NAME1 TASK_NAME2
```
