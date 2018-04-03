FROM python:3.5

ENV APP_ROOT /usr/src/app
ENV APP_USER_NAME app
ENV APP_USER_UID 1000

# Prepare environment
RUN useradd -m -d ${APP_ROOT} \
    --shell /bin/bash \
    --uid ${APP_USER_UID} \
    ${APP_USER_NAME}
RUN mkdir -p ${APP_ROOT}
RUN mkdir -p /var/log/eventol
RUN chown ${APP_USER_NAME}:root /var/log/eventol
WORKDIR ${APP_ROOT}

# Install nodejs and gettext
ENV NODE_VERSION 8.x
RUN curl -sL https://deb.nodesource.com/setup_${NODE_VERSION} | bash -
RUN apt-get install -y nodejs gettext \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python requirements
COPY ./requirements.txt ${APP_ROOT}
COPY ./requirements-dev.txt ${APP_ROOT}
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN pip install psycopg2

# Install node modules
COPY ./eventol/front/package.json ${APP_ROOT}/eventol/front/
COPY ./eventol/front/yarn.lock ${APP_ROOT}/eventol/front/
RUN npm install -g yarn webpack@^1.12.13
RUN cd ${APP_ROOT}/eventol/front && yarn install

# Install bower dependencies
COPY ./eventol/front/bower.json ${APP_ROOT}/eventol/front/
COPY ./eventol/front/.bowerrc ${APP_ROOT}/eventol/front/
RUN npm install -g bower
RUN cd ${APP_ROOT}/eventol/front && bower install --allow-root

# Copy test script file
COPY ./test.sh ${APP_ROOT}/test.sh

# Copy python code
COPY ./eventol ${APP_ROOT}/eventol
RUN mkdir -p ${APP_ROOT}/eventol/manager/static
RUN mkdir -p ${APP_ROOT}/eventol/front/eventol/static

# Compile scss
RUN npm install -g less
RUN mkdir -p ${APP_ROOT}/eventol/manager/static/manager/css/
RUN lessc ${APP_ROOT}/eventol/front/eventol/static/manager/less/eventol.less > ${APP_ROOT}/eventol/manager/static/manager/css/eventol.css
RUN lessc ${APP_ROOT}/eventol/front/eventol/static/manager/less/eventol-bootstrap.less > ${APP_ROOT}/eventol/manager/static/manager/css/eventol-bootstrap.css

# Copy script for docker-compose wait and start-eventol
COPY ./deploy/docker/scripts/wait-for-it.sh ${APP_ROOT}/wait-for-it.sh
COPY ./deploy/docker/scripts/start_eventol.sh ${APP_ROOT}/start_eventol.sh

# Compile reactjs code
RUN cd ${APP_ROOT}/eventol/front && webpack --config webpack.prod.config.js

# Collect statics
RUN mkdir -p ${APP_ROOT}/eventol/static
RUN cd ${APP_ROOT}/eventol && python manage.py collectstatic --noinput

# Create media folder
RUN mkdir -p ${APP_ROOT}/eventol/media

# Chown files
RUN chmod 0750 ${APP_ROOT}
RUN chown --recursive ${APP_USER_NAME}:${APP_USER_NAME} ${APP_ROOT}

# Drop privs
USER ${APP_USER_NAME}

# Create log file
RUN touch /var/log/eventol/eventol.log

# Compile .po files
RUN sed -i 's@#~ @@g' ${APP_ROOT}/eventol/conf/locale/*/LC_MESSAGES/djangojs.po
RUN cd ${APP_ROOT}/eventol && python manage.py compilemessages

EXPOSE 8000

VOLUME ${APP_ROOT}/eventol/media
VOLUME ${APP_ROOT}/eventol/static


CMD ["tail", "-f", "/dev/null"]
