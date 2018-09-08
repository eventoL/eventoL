# Eventol

## Status

[![pipeline status](https://github.com/eventol/eventol/badges/master/pipeline.svg)](https://github.com/eventol/eventol/commits/master)
[![coverage report](https://github.com/eventol/eventol/badges/master/coverage.svg)](https://github.com/eventol/eventol/commits/master)

## Setup developer mode
```
cp .env.dist .env (Customize if necessary)
cp ./eventol/front/webpack.local-settings.js{.sample,}
docker-compose up -d --build
```

## This creates 3 different containers
```
      Name                    Command               State                Ports
--------------------------------------------------------------------------------------------
eventol_reactjs_1   npm start                        Up                  0.0.0.0:3000->3000/tcp, 8000/tcp
eventol_redis_1     docker-entrypoint.sh redis ...   Up                  0.0.0.0:32779->6379/tcp
eventol_worker_1    python manage.py runserver ...   Up                  0.0.0.0:8000->8000/tcp
```

## Running the django server
```
docker-compose exec worker ./deploy/scripts/install-container-dev.sh
docker-compose exec worker python eventol/manage.py runserver 0.0.0.0:8000
```

## Running the frontend
```
docker-compose exec reactjs yarn install
docker-compose exec reactjs yarn start
```

## To see the logs of any of them:
```
docker-compose logs -f [reactjs|worker|redis]
```

The source code is available under the src directory
By default it uses an sqlite db, with data already on it
```
*default user*: admin
*password*: passw0rda
```

Note: Each time something is pushed to the repository, gitlab registry builds a new image and tags it. In order to use the containers in development mode, is always necessary to recreate them each time a library is added using docker-compose build

master:
=======
 registry.gitlab.com/eventol-team/eventol:latest
 registry.gitlab.com/eventol-team/eventol:YYYY.MM.DD-HH.mm.ss

dev:
=====
 registry.gitlab.com/eventol-team/eventol:latest-dev
 registry.gitlab.com/eventol-team/eventol:YYYY.MM.DD-HH.mm.ss-dev

## Translations

Every time a new string is generated on the source code, you'll need to
generate the translation files

### Create .po files with  translation string

# Javascript and reactjs translations
```
(first time) docker-compose exec worker python manage.py makemessages -l es --no-location
(later times) docker-compose exec worker python manage.py makemessages -a --no-location
```

### Compile translations files
```
docker-compose exec worker python manage.py compilemessages
```

## Setup production mode

Although production mode is only meant for servers. Sometimes could be useful
to test an specific image

## Install of eventol (production mode) The version of the tag should match the one on the .env file
```
docker build . -t registry.gitlab.com/eventol-team/eventol:latest
```

## Customize environment variables (You )
```
cp .env.dist .env
```

## Start containers
```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

# Uploading default configuration
```
docker-compose exec worker python manage.py loaddata fixtures/initial_users.json
docker-compose exec worker python manage.py loaddata fixtures/initial_config.json
```

## Create a new user
```
docker-compose exec worker python manage.py createsuperuser
```
