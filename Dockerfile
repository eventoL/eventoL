#########################################
# frontend image
#########################################
FROM node:12.12.0-alpine as frontend

## Install system dependencies
RUN apk --update add --no-cache \
    git gcc make autoconf automake musl-dev zlib zlib-dev\
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /app
RUN chown -R node:node /app

# Set user
USER node

# Install yarn dependencies
COPY --chown=node:node ./eventol/front/package.json ./eventol/front/yarn.lock ./
RUN yarn install

# Copy code
COPY --chown=node:node ./eventol/front/ .

# Build
RUN yarn build

EXPOSE 3000

CMD ["tail", "-f", "/dev/null"]

#########################################
# build image
#########################################
FROM python:3.9.0-alpine as development

# Set environment variables
ENV APP_ROOT /usr/src/app/
ENV IS_ALPINE true
ENV DJANGO_CONFIGURATION=Prod

# Install system dependencies
RUN apk --update add --no-cache \
  bash git gcc cairo-dev postgresql-dev libxslt-dev \
  gettext musl-dev py3-setuptools jpeg-dev make \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Install python dependencies
RUN pip3 install --no-cache-dir cffi cairocffi psycopg2
RUN apk --update add --no-cache cairo-dev \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create folders for deploy
RUN mkdir -p ${APP_ROOT}
RUN mkdir -p /var/log/eventol
WORKDIR ${APP_ROOT}

# Create user
RUN adduser -D -h ${APP_ROOT} -s /bin/bash app
RUN chown app:app /var/log/eventol

# Install python requirements
COPY --chown=app:app ./requirements.txt ./requirements-dev.txt ${APP_ROOT}
RUN pip3 install --no-cache-dir -r requirements-dev.txt

# Set user
USER app

# Copy python code
COPY --chown=app:app ./Makefile ${APP_ROOT}/Makefile
COPY --chown=app:app ./eventol ${APP_ROOT}/eventol
RUN mkdir -p ${APP_ROOT}/eventol/manager/static
RUN mkdir -p ${APP_ROOT}/eventol/front/eventol/static

# Copy frontend files
COPY --chown=app:app --from=frontend /app/webpack-stats-prod.json ${APP_ROOT}/eventol/front/webpack-stats-prod.json
COPY --chown=app:app --from=frontend /app/eventol/static ${APP_ROOT}/eventol/front/eventol/static

# Copy script for docker-compose wait and start-eventol
COPY --chown=app:app ./deploy/docker/scripts/wait-for-it.sh ${APP_ROOT}/wait-for-it.sh
COPY --chown=app:app ./deploy/docker/scripts/start_eventol.sh ${APP_ROOT}/start_eventol.sh

# Collect statics
RUN mkdir -p ${APP_ROOT}/eventol/static
RUN cd ${APP_ROOT}/eventol && python manage.py collectstatic --noinput

# Create media folder
RUN mkdir -p ${APP_ROOT}/eventol/media

# Create log file
RUN touch /var/log/eventol/eventol.log

# Compile .po files
RUN sed -i 's@#~ @@g' ${APP_ROOT}/eventol/conf/locale/*/LC_MESSAGES/djangojs.po
RUN cd ${APP_ROOT}/eventol && python manage.py compilemessages

EXPOSE 8000

VOLUME ${APP_ROOT}/eventol/media
VOLUME ${APP_ROOT}/eventol/static

CMD ["tail", "-f", "/dev/null"]
