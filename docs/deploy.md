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

#### Postgres:
- PSQL_NAME (Default: **eventol**)
- PSQL_USER (Default: **eventol**)
- PSQL_PASSWORD (Default: **secret**)
- PSQL_HOST (Default: **localhost**)
- PSQL_PORT (Default: **5432**)

### Deploy con Docker
TODO

### Deploy con Docker-Compose
TODO

### Deploy en servidor
TODO
