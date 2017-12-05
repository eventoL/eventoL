cd eventol
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata manager/initial_data/attendee_data.json
./manage.py loaddata manager/initial_data/email_addresses.json
./manage.py loaddata manager/initial_data/initial_data.json
./manage.py loaddata manager/initial_data/security.json
./manage.py loaddata manager/initial_data/software.json
./manage.py collectstatic --no-input
./manage.py runserver 0.0.0.0:8000

