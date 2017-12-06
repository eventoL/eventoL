# Esta es la instalación para modo desarrollo
Hay dos opciones:
- Con docker (recomendada)
- Directamente en tu maquina

## Con Docker

### Obtener imagen de docker
Podes crear la tuya o tomar la generada de docker hub.

#### Tomar la imagen de docker hub
```bash
docker pull eventol/eventol:latest
```

#### Crear imagen local con todas las dependencias
```bash
docker build --tag=eventol/eventol:latest .
```

### Correr un container con esa imagen
```bash
docker run -d -it --name eventol -v $PWD:/src -p 8000:8000 --workdir /src eventol/eventol:latest bash
```

### Crear la base de datos y actualizar estaticos
```bash
docker exec -it eventol ./deploy/scripts/install-container-dev.sh
```

### Correr el servidor para probar y desarrollar
```bash
docker exec -it eventol ./eventol/manage.py runserver 0.0.0.0:8000
```

## Sin docker

### Npm
Nosotros estamos usando npm para las dependencias del frontend
* [Instalar npm y nodejs](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager)

### Python 3
Nosotros estamos usando python 3.5 para correr el proyecto

### Instalar dependencias, crear la base de datos y actualizar estaticos

#### Hacerlo desde script
```bash
./deploy/scripts/install.sh
```

#### Hacerlo manualmente
```bash
#virtualenv -p python3 venv
#source venv/bin/activate
pip3 install -r requirements.txt -r requirements-dev.txt
cd eventol
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata manager/initial_data/attendee_data.json
./manage.py loaddata manager/initial_data/email_addresses.json
./manage.py loaddata manager/initial_data/initial_data.json
./manage.py loaddata manager/initial_data/security.json
./manage.py loaddata manager/initial_data/software.json

sudo npm install -g less bower
# sudo npm install -g yarn
cd front
# yarn install
bower install
lessc eventol/static/manager/less/flisol.less > ../manager/static/manager/css/flisol.css
lessc eventol/static/manager/less/flisol-bootstrap.less > ../manager/static/manager/css/flisol-bootstrap.css
cd -

./manage.py collectstatic --no-input
```

### Correr el servidor para probar y desarrollar
```bash
./eventol/manage.py runserver 0.0.0.0:8000
```

# Actualizar traducciones

## Con Docker
```bash
docker exec -it eventol ./eventol/manage.py makemessages --locale=es
docker exec -it eventol ./eventol/manage.py compilemessages
```

## Sin Docker
```bash
django-admin makemessages --locale=es
django-admin compilemessages
```

# Configuración para inicio de sesión desde redes sociales

Una vez iniciado el server, visitamos la pagina de administración (Ejemplo: `http://localhost:8000/admin/`) y seguir los siguientes pasos:

* Añadir un sitio para su dominio, que se corresponda con `settings.SITE_ID` (` django.contrib.sites app`).
* Para cada proveedor basado en OAuth, añadir un Social App (socialaccount app).
* Complete los datos con el sitio y las credenciales de aplicaciones OAuth obtenidos del proveedor.

Para cualquier problema con las cuentas sociales, por favor verifique en la [documentación de django-allauth](http://django-allauth.readthedocs.org).
