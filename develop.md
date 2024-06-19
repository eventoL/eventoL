# import _tkinter # If this fails your Python may not be configured for Tk	
# sudo apt install python3-tk tk-dev

pyenv install 3.9.6
pyenv shell 3.9.6

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install "setuptools<58.0.0" wheel --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir

cd eventol
./manage.py migrate

mkdir -p ../eventol/static
mkdir -p ../eventol/front/eventol/static
./manage.py collectstatic --noinput

./manage.py createsuperuser

./manage.py runserver 0.0.0.0:8000

