# EventoL Deploy

For a better and faster production implementation, **EventoL** is configurable through environment variables so that during the deployment the code doesn't have to be modified.

## **EventoL** environment variables

### Docker and Django:
- HOST (Default: **localhost**)
- EXTERNAL_PORT (Default: 80)
- DOCKER_IMAGE_NAME (Default: **eventol/eventol**)
- DOCKER_IMAGE_VERSION (Default: **latest**)
- APP_DNS (Default: **localhost**)

### Django:
- DEBUG (Default: **False**)
- TEMPLATE_DEBUG (Default: **False**)
- EMAIL_BACKEND (Default: **django.core.mail.backends.console.EmailBackend**)
- EMAIL_HOST (Default: **smtp.unset**)
- EMAIL_PORT (Default: **587**)
- EMAIL_HOST_USER (Default: **change_unset@mail.com**)
- EMAIL_HOST_PASSWORD (Default: **secret**)
- EMAIL_FROM (Default: **change_unset@mail.com**)
- ALLOWED_HOSTS (Default: **['*']**)
- SECRET_KEY (Default: **6(15by=#xqa2r-@-qqjc%gwo(y2#$66-)#)&w3j%+!ax3n+2v1**)
- LANGUAGE_CODE (Default: **en-US**)
- TIME_ZONE (Default: **UTC**)
- RECAPTCHA_USE_SSL (Default: **False**)
- REDIS_HOST (Default: **redis**)
- REDIS_PORT (Default: **6379**)
- EMAIL_USE_TLS (Default: **True**)
- ADMIN_TITLE (Default: **EventoL**)
- PRIVATE_ACTIVITIES (Default: **False** )

### Postgres:
- PSQL_DBNAME (Default: **eventol**)
- PSQL_USER (Default: **eventol**)
- PSQL_PASSWORD (Default: **secret**)
- PSQL_HOST (Default: **localhost**)
- PSQL_PORT (Default: **5432**)

## Deploy with Docker-Compose

### All commands are executed in to **deploy/docker** folder

### Update environment variebles
```bash
cp .env.dist .env
# Change your variables in .env file
source .env
```

### Build nginx image with configuration
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
```

### Build EventoL image
Only run this step when you want run local code in production mode
```bash
docker build --tag=eventol/eventol:latest .
```

### Deploy
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Create admin user
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec worker python manage.py createsuperuser
```

## Result

### Containers running
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

Name                     Command               State            Ports
------------------------------------------------------------------------------------
docker_daphne_1     bash -c cd eventol; daphne ...   Up      8000/tcp
docker_nginx_1      /usr/sbin/nginx                  Up      0.0.0.0:80->80/tcp
docker_postgres_1   docker-entrypoint.sh postgres    Up      0.0.0.0:32790->5432/tcp
docker_redis_1      docker-entrypoint.sh redis ...   Up      0.0.0.0:32791->6379/tcp
docker_worker_1     /root/wait-for-it.sh -p 54 ...   Up      8000/tcp
```

### Server run in: **http://localhost/** (if you didn't change the HOST variable in your environment)
