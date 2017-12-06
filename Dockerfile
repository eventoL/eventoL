FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install nodejs and gettext
ENV NODE_VERSION 8.x
RUN curl -sL https://deb.nodesource.com/setup_${NODE_VERSION} | bash -
RUN apt-get install -y nodejs gettext \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python requirements
COPY ./requirements.txt /usr/src/app/
COPY ./requirements-dev.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN pip install psycopg2

# Install node modules
COPY ./eventol/front/package.json /usr/src/app/eventol/front/
COPY ./eventol/front/yarn.lock /usr/src/app/eventol/front/
RUN npm install -g yarn webpack
RUN cd /usr/src/app/eventol/front && yarn install

# Install bower dependencies
COPY ./eventol/front/bower.json /usr/src/app/eventol/front/
COPY ./eventol/front/.bowerrc /usr/src/app/eventol/front/
RUN npm install -g bower
RUN cd /usr/src/app/eventol/front && bower install --allow-root

# Copy test script file
COPY ./test.sh /usr/src/app/test.sh

# Copy python code
COPY ./eventol /usr/src/app/eventol
RUN mkdir -p /usr/src/app/eventol/manager/static
RUN mkdir -p /usr/src/app/eventol/front/eventol/static

# Compile scss
RUN npm install -g less
RUN mkdir -p /usr/src/app/eventol/manager/static/manager/css/
RUN lessc /usr/src/app/eventol/front/eventol/static/manager/less/flisol.less > /usr/src/app/eventol/manager/static/manager/css/flisol.css
RUN lessc /usr/src/app/eventol/front/eventol/static/manager/less/flisol-bootstrap.less > /usr/src/app/eventol/manager/static/manager/css/flisol-bootstrap.css

# Copy script for docker-compose wait and start-eventol
COPY ./deploy/docker/scripts/wait-for-it.sh /root
COPY ./deploy/docker/scripts/start_eventol.sh /usr/src/app/start_eventol.sh

# Compile reactjs code
RUN cd /usr/src/app/eventol/front && webpack --config webpack.prod.config.js

# Collect statics
RUN cd /usr/src/app/eventol && python manage.py collectstatic --noinput

# Compile .po files
RUN sed -i 's@#~ @@g' /usr/src/app/eventol/conf/locale/*/LC_MESSAGES/djangojs.po
RUN cd /usr/src/app/eventol && python manage.py compilemessages

EXPOSE 8000

VOLUME /usr/src/app

CMD ["tail", "-f", "/dev/null"]
