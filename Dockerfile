FROM python:3.5-alpine

# Set environment variables
ENV APP_ROOT /usr/src/app
ENV APP_USER_NAME app
ENV APP_USER_UID 1000
ENV IS_ALPINE true
ENV NODE_VERSION 8.x

# Install alpine dependencies

## Upgrade apk-tools
RUN apk add --upgrade --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main apk-tools

## Install system dependencies
RUN apk --update add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
    bash wget dpkg-dev libffi nodejs nodejs-npm git gcc musl-dev gettext \
    openssl-dev postgresql-dev libffi-dev py3-setuptools jpeg-dev make \
    zlib-dev freetype-dev lcms2-dev openjpeg-dev libxslt-dev alpine-sdk \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Install react dependencies
RUN npm install -g npm
RUN npm install -g yarn webpack@^1.12.13 bower less

## Install python dependencies
RUN pip3 install --no-cache-dir cffi cairocffi psycopg2
RUN apk --update add --no-cache cairo-dev \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user
RUN adduser -D -h ${APP_ROOT} \
    -s /bin/bash \
    -u ${APP_USER_UID} \
    ${APP_USER_NAME}

# Create folders for deploy
RUN mkdir -p ${APP_ROOT}
RUN mkdir -p /var/log/eventol
RUN chown ${APP_USER_NAME}:root /var/log/eventol
WORKDIR ${APP_ROOT}

# Install python requirements
COPY ./requirements.txt ${APP_ROOT}
COPY ./requirements-dev.txt ${APP_ROOT}
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements-dev.txt

# Install node modules
COPY ./eventol/front/package.json ${APP_ROOT}/eventol/front/
COPY ./eventol/front/yarn.lock ${APP_ROOT}/eventol/front/
RUN cd ${APP_ROOT}/eventol/front && yarn install
RUN cd ${APP_ROOT}/eventol/front && npm rebuild node-sass --force

# Install bower dependencies
COPY ./eventol/front/bower.json ${APP_ROOT}/eventol/front/
COPY ./eventol/front/.bowerrc ${APP_ROOT}/eventol/front/
RUN cd ${APP_ROOT}/eventol/front && bower install --allow-root

# Copy test script file
COPY ./test.sh ${APP_ROOT}/test.sh

# Copy python code
COPY ./eventol ${APP_ROOT}/eventol
RUN mkdir -p ${APP_ROOT}/eventol/manager/static
RUN mkdir -p ${APP_ROOT}/eventol/front/eventol/static

# Compile scss
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

# Clean and chown files
RUN rm -rf ${APP_ROOT}/eventol/front \
  && mkdir -p ${APP_ROOT}/eventol/front
RUN chmod 0755 ${APP_ROOT}
RUN chown --changes --recursive ${APP_USER_NAME}:${APP_USER_NAME} ${APP_ROOT}/

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
