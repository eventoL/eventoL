# Esta es la instalación para modo desarrollo
Solo se puede instalar con docker y docker-compose

## Requirements

- **make**: [documentación](https://www.gnu.org/software/make/)
- **docker**: [instalación](https://docs.docker.com/install/)
- **docker-compose**: [instalación](https://docs.docker.com/compose/install/)

### Setup developer mode

```bash
make deploy-dev
```

### This creates 4 different containers

```bash
      Name                     Command               State           Ports
-----------------------------------------------------------------------------------
docker_postgres_1   docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
docker_reactjs_1    docker-entrypoint.sh tail  ...   Up      0.0.0.0:3000->3000/tcp
docker_redis_1      docker-entrypoint.sh redis ...   Up      6379/tcp
docker_worker_1     tail -f /dev/null                Up      0.0.0.0:8000->8000/tcp
```

### Running the django server

```bash
make migrate
make setup-frontend
make collectstatic
make runserver
```

### Running the frontend

```bash
make setup-frontend
make start-frontend
```

### Para ver la instancia local de eventoL

```bash
http://localhost:8000
```

### Para parar el sistema

```bash
make stop-dev
```

### Para apagar los contenedores y limpiar el entorno (no los volumenes de la base de datos)

```bash
make undeploy-dev
```

### Para apagar los contenedores, limpiar el entorno y BORRAR TODA LOS DATOS

```bash
make undeploy-full-dev
```

### Para reiniciar una vez configurado

```bash
make restart

# cada uno de los siguientes en terminales diferentes
make runserver
make start-frontend
```

### To see the logs of any of them

```bash
make logs-dev
```

### To see and follow the logs of any of them

```bash
make logs-follow-dev
```

# Actualizar traducciones

## Con Docker

```bash
make make-translations
make compile-translations
```

## Sin Docker

```bash
make backend-make-translations
make backend-compile-translations
```

## Configuración para inicio de sesión desde redes sociales

Una vez iniciado el server, visitamos la pagina de administración (Ejemplo: `http://localhost:8000/admin/`) y seguir los siguientes pasos:

- Añadir un sitio para su dominio, que se corresponda con `settings.SITE_ID` (` django.contrib.sites app`).
- Para cada proveedor basado en OAuth, añadir un Social App (socialaccount app).
- Complete los datos con el sitio y las credenciales de aplicaciones OAuth obtenidos del proveedor.

Para cualquier problema con las cuentas sociales, por favor verifique en la [documentación de django-allauth](http://django-allauth.readthedocs.org).

## Configurar visibilidad de actividades

Utilizando la setting `PRIVATE_ACTIVITIES` se puede controlar si el listado de actividades es publico o únicamente accesible por organizadores.
