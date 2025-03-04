# Eventol

## Status

[![pipeline status](https://github.com/eventol/eventol/badges/master/pipeline.svg)](https://github.com/eventol/eventol/commits/master)
[![coverage report](https://github.com/eventol/eventol/badges/master/coverage.svg)](https://github.com/eventol/eventol/commits/master)

## Setup developer mode

```bash
mkdir -p db/postgres
cp .env.dist .env (Customize if necessary)

docker compose pull
docker compose build --force-rm
docker compose up -d --build
```

## This creates 5 different containers

```bash
      Name                    Command               State                Ports
--------------------------------------------------------------------------------------------
docker_postgres_1        docker-entrypoint.sh postgres    Up      5432/tcp
docker_redis_1           docker-entrypoint.sh redis ...   Up      6379/tcp
docker_worker_1          tail -f /dev/null                Up      0.0.0.0:8000->8000/tcp
```

## Running the django server

```bash
docker compose exec worker ./deploy/scripts/install-container-dev.sh
docker compose exec worker python eventol/manage.py runserver 0.0.0.0:8000
```

## To see the logs of any of them:

```bash
docker compose logs -f [worker|redis]
```

The source code is available under the src directory
By default it uses an sqlite db, with data already on it

```bash
*default user*: admin
*password*: passw0rda
```

Note: Each time something is pushed to the repository, gitlab registry builds a new image and tags it. In order to use the containers in development mode, is always necessary to recreate them each time a library is added using docker compose build

### master

 registry.gitlab.com/eventol-team/eventol:latest
 registry.gitlab.com/eventol-team/eventol:YYYY.MM.DD-HH.mm.ss

### dev

 registry.gitlab.com/eventol-team/eventol:latest-dev
 registry.gitlab.com/eventol-team/eventol:YYYY.MM.DD-HH.mm.ss-dev

## Translations

Every time a new string is generated on the source code, you'll need to
generate the translation files

### Create .po files with  translation string

```bash
(first time) docker compose exec worker python manage.py makemessages -l es --no-location
(later times) docker compose exec worker python manage.py makemessages -a --no-location
```

### Compile translation files

```bash
docker compose exec worker python manage.py compilemessages
```

## Setup production mode

Although production mode is only meant for servers. Sometimes could be useful
to test an specific image

## Install of eventol (production mode) The version of the tag should match the one on the .env file

```bash
docker build . -t registry.gitlab.com/eventol-team/eventol:latest
```

## Customize environment variables (You )

```bash
cp .env.dist .env
```

## Start containers

```bash
docker compose -f docker-compose.prod.yml up -d
```

### Uploading default configuration

```bash
docker compose exec worker python manage.py loaddata fixtures/initial_users.json
docker compose exec worker python manage.py loaddata fixtures/initial_config.json
```

#### Create a new user

```bash
docker compose exec worker python manage.py createsuperuser
```
