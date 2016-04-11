## Deploy de EventoL

Para un mejor y mas rápido deploy a producción, **EventoL** es configurable mediante variables de entorno para que durante el deploy el codigo no se tenga que modificar.

### Variables de entorno de **EventoL**

#### Django:

- DJANGO_DEBUG (Default: **False**)
- DJANGO_TEMPLATE_DEBUG (Default: **False**)
- DJANGO_EMAIL_HOST (Default: **smtp.unset**)
- DJANGO_EMAIL_PORT (Default: **587**)
- DJANGO_EMAIL_HOST_USER (Default: **change_unset@mail.com**)
- DJANGO_EMAIL_HOST_PASSWORD (Default: **secret**)
- DJANGO_EMAIL_USE_TLS (Default: **True**)
- DJANGO_EMAIL_FROM (Default: **change_unset@mail.com**)
- DJANGO_ADMIN_TITLE (Default: **EventoL**)
- DJANGO_SECRET_KEY (Default: **!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu**)

#### Postgres:
- PSQL_NAME (Default: **eventol**)
- PSQL_USER (Default: **eventol**)
- PSQL_PASSWORD (Default: **secret**)
- PSQL_HOST (Default: **localhost**)
- PSQL_PORT (Default: **5432**)

#### Openshift:
- OPENSHIFT_REPO_DIR configura las variables STATIC_ROOT y MEDIA_ROOT 
- OPENSHIFT_SECRET_TOKEN configura la varible DJANGO_SECRET_KEY
- OPENSHIFT_APP_NAME configura la varible PSQL_NAME
- OPENSHIFT_POSTGRESQL_DB_USERNAME configura la varible PSQL_USER
- OPENSHIFT_POSTGRESQL_DB_PASSWORD configura la varible PSQL_PASSWORD
- OPENSHIFT_POSTGRESQL_DB_HOST configura la varible PSQL_HOST
- OPENSHIFT_POSTGRESQL_DB_PORT configura la varible PSQL_PORT
- OPENSHIFT_APP_DNS configura la varible ALLOWED_HOSTS
- OPENSHIFT_DATA_DIR

#### Otras configuraciones para mail:
- EVENTOL_EMAIL_BACKEND
- EVENTOL_MAILGUN_ACCESS_KEY
- EVENTOL_MAILGUN_SERVER_NAME

### Deploy con Docker
```bash
cd deploy/docker
docker build -t eventol .
docker run --name eventol-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=eventol -e POSTGRES_DB=eventol -p 5432:5432 -d postgres
docker run -d -i --name="eventol" --hostname="eventol" -p 8000:8000 --link=eventol-postgres -e PSQL_HOST=eventol-postgres -t eventol:latest
```

### Deploy con Docker-Compose
```bash
cd deploy/docker
docker-compose build
docker-compose run -d
```

### Deploy en servidor
**TODO**