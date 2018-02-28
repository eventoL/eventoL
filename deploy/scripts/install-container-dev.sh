cd eventol
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata manager/initial_data/attendee_data.json
./manage.py loaddata manager/initial_data/email_addresses.json
./manage.py loaddata manager/initial_data/initial_data.json
./manage.py loaddata manager/initial_data/security.json
./manage.py loaddata manager/initial_data/software.json

cd front
# yarn install
bower install --allow-root
lessc eventol/static/manager/less/eventol.less > ../manager/static/manager/css/eventol.css
lessc eventol/static/manager/less/eventol-bootstrap.less > ../manager/static/manager/css/eventol-bootstrap.css
cd -

./manage.py collectstatic --no-input

