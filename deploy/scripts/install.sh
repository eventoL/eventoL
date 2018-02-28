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
lessc eventol/static/manager/less/eventol.less > ../manager/static/manager/css/eventol.css
lessc eventol/static/manager/less/eventol-bootstrap.less > ../manager/static/manager/css/eventol-bootstrap.css
cd -

./manage.py collectstatic --no-input
