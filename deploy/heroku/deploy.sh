export NODE_ENV=development
cd eventol/front
npm install -g yarn
yarn install
node_modules/.bin/webpack --config webpack.local.config.js
cd -
python eventol/manage.py migrate
python eventol/manage.py collectstatic --noinput
python eventol/manage.py loaddata data/social.json
python eventol/manage.py loaddata data/users.json
python eventol/manage.py loaddata eventol/manager/initial_data/attendee_data.json
python eventol/manage.py loaddata eventol/manager/initial_data/email_addresses.json
python eventol/manage.py loaddata eventol/manager/initial_data/initial_data.json
python eventol/manage.py loaddata eventol/manager/initial_data/security.json
python eventol/manage.py loaddata eventol/manager/initial_data/software.json
python eventol/manage.py runserver "0.0.0.0:$PORT"
