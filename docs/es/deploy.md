## Deploy de EventoL

## Customize environment variables (You )
```
cd deploy/docker
cp .env.dist .env
source .env
docker build --tag=eventol/eventol:latest .
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Start containers
```
$ docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

# Uploading default configuration

```
$ docker-compose exec worker python manage.py loaddata fixtures/initial_users.json
$ docker-compose exec worker python manage.py loaddata fixtures/initial_config.json
```

## Create a new user

```
$ docker-compose exec worker python manage.py createsuperuser
```
