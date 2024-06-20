# Instalación de desarrollo

## Instalar pyenv

- URL: (pyenv/pyenv)[https://github.com/pyenv/pyenv]

```bash
curl https://pyenv.run | bash
```

## python 3.9.6

```bash
pyenv install 3.9.6
pyenv shell 3.9.6
```

## Entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar las dependencias

```bash
pip install --upgrade pip
pip install "setuptools<58.0.0" wheel
pip install -r requirements-pycamp.txt
```

### Errores posibles

- **import _tkinter # If this fails your Python may not be configured for Tk	**: solución `sudo apt install python3-tk tk-dev`

## Correr el proyecto

```bash
cd eventol
./manage.py migrate

mkdir -p ../eventol/static
mkdir -p ../eventol/front/eventol/static
./manage.py collectstatic --noinput

./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```
