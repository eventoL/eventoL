# Deploy de EventoL

Para un mejor y mas rápido deploy a producción, **EventoL** es configurable mediante variables de entorno para que durante el deploy el codigo no se tenga que modificar.

## Variables de entorno de **EventoL**

### Docker y Django:
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

## Deploy con Docker-Compose

### Todo esto se ejecuta dentro de la carpeta **deploy/docker**

### Actualizar las varibles de entorno
```bash
cp .env.dist .env
# Cambiar variables en .env si hay algun valor distinto que quieras tener en tu entorno
source .env
```

### Generar la imagen de nginx con la configuración
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
```

### Generar la imagen de EventoL
Solo hacer este paso si queres correr el servidor en modo producción con el codigo local
```bash
docker build --tag=eventol/eventol:latest .
```

### Hacer el deploy completo
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Crear usuario administrador
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec worker python manage.py createsuperuser
```

## Resultado

### Containers corriendo
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

### Servidor andando en: **http://localhost/** (si no cambiaste el HOST en las varibles de entorno)
