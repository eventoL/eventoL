#########################################
# build image
#########################################
FROM python:3.9.6-alpine3.13

# Set environment variables
ENV APP_ROOT /usr/src/app/
ENV IS_ALPINE true
ENV DJANGO_CONFIGURATION=Prod

# Install system dependencies
RUN apk --update add --no-cache \
  bash git gcc cairo-dev postgresql-dev libxslt-dev gcc cargo gdal-dev gdal sox flite \
  gettext musl-dev py3-setuptools jpeg-dev make python3-dev libffi-dev openssl-dev \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir cffi cairocffi psycopg2
RUN apk --update add --no-cache cairo-dev \
  && rm -rf /var/cache/apk/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create folders for deploy
RUN mkdir -p ${APP_ROOT}
RUN mkdir -p /var/log/eventol
WORKDIR ${APP_ROOT}

# Install python requirements
COPY ./requirements.txt ./requirements-dev.txt ${APP_ROOT}
RUN pip3 install --no-cache-dir -r requirements-dev.txt
RUN pip3 install psycopg2-binary gunicorn

# Copy python code
COPY ./Makefile ${APP_ROOT}/Makefile
COPY ./eventol ${APP_ROOT}/eventol
RUN mkdir -p ${APP_ROOT}/eventol/manager/static
RUN mkdir -p ${APP_ROOT}/eventol/front/eventol/static

# Copy git files
COPY ./.git ${APP_ROOT}/.git

# Copy script for docker-compose wait and start-eventol
COPY ./deploy/docker/scripts/wait-for-it.sh ${APP_ROOT}/wait-for-it.sh
COPY ./deploy/docker/scripts/start_eventol.sh ${APP_ROOT}/start_eventol.sh

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
