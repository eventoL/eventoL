# Esta es la instalación para modo desarrollo
Solo se puede instalar con docker y docker-compose

### Setup developer mode
```
cd deploy/docker
cp .env.dist .env

docker-compose pull
docker-compose build --force-rm
docker-compose up -d --build
```

### This creates 5 different containers
```
      Name                    Command               State                Ports
--------------------------------------------------------------------------------------------
docker_daphne_1     bash -c cd eventol; daphne ...   Up      8000/tcp
docker_postgres_1   docker-entrypoint.sh postgres    Up      0.0.0.0:32790->5432/tcp
docker_redis_1      docker-entrypoint.sh redis ...   Up      0.0.0.0:32791->6379/tcp
docker_worker_1     /root/wait-for-it.sh -p 54 ...   Up      8000/tcp
docker_elasticsearch_1     ...                       Up      9300/tcp 9200/tcp
```

### Running the django server
```
docker-compose exec worker python eventol/manage.py migrate
docker-compose exec worker python eventol/manage.py collectstatic
docker-compose exec worker python eventol/manage.py runserver 0.0.0.0:8000
```

### Running the frontend
```
docker-compose exec reactjs yarn install
docker-compose exec reactjs yarn start
```

### To see the logs of any of them:
```
docker-compose logs -f [reactjs|worker|redis]
```

# Actualizar traducciones

## Con Docker
```bash
docker exec -it eventol ./eventol/manage.py makemessages --locale=es
docker exec -it eventol ./eventol/manage.py compilemessages
```

## Sin Docker
```bash
cd eventol
django-admin makemessages --locale=es
django-admin compilemessages
cd -
```

# Configuración para inicio de sesión desde redes sociales

Una vez iniciado el server, visitamos la pagina de administración (Ejemplo: `http://localhost:8000/admin/`) y seguir los siguientes pasos:

* Añadir un sitio para su dominio, que se corresponda con `settings.SITE_ID` (` django.contrib.sites app`).
* Para cada proveedor basado en OAuth, añadir un Social App (socialaccount app).
* Complete los datos con el sitio y las credenciales de aplicaciones OAuth obtenidos del proveedor.

Para cualquier problema con las cuentas sociales, por favor verifique en la [documentación de django-allauth](http://django-allauth.readthedocs.org).

# Configurar visibilidad de actividades

Utilizando la setting `PRIVATE_ACTIVITIES` se puede controlar si el listado de actividades es publico o únicamente accesible por organizadores.
