#########################################
# build image
#########################################
FROM python:3.12-slim-bookworm

# Set environment variables
ENV APP_ROOT=/usr/src/app/

# Install system dependencies using apt-get
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bash git gcc libc6-dev libcairo2-dev libpq-dev libxslt1-dev cargo gdal-bin \
    sox flite gettext build-essential pkg-config default-jdk unzip wget python3 python3-pip \
    libffi-dev libssl-dev libxmlsec1-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir cffi cairocffi psycopg2

# Additional installation for cairo-dev equivalent
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends libcairo2-dev && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip3 install uv

# Create folders for deploy
RUN mkdir -p ${APP_ROOT}
RUN mkdir -p /var/log/eventol
WORKDIR ${APP_ROOT}

# Copy pyproject.toml and uv.lock
COPY ./pyproject.toml ./uv.lock ${APP_ROOT}/

# Install dependencies with uv
RUN uv sync --frozen --no-dev

# Copy python code
COPY ./Makefile ${APP_ROOT}/Makefile
COPY ./eventol ${APP_ROOT}/eventol
RUN mkdir -p ${APP_ROOT}/eventol/manager/static

# Copy git files
COPY ./.git ${APP_ROOT}/.git

# Copy script for docker-compose wait, start-eventol and start-celery
COPY ./deploy/docker/scripts/wait-for-it.sh ${APP_ROOT}/wait-for-it.sh
COPY ./deploy/docker/scripts/start_eventol.sh ${APP_ROOT}/start_eventol.sh
COPY ./deploy/docker/scripts/start_celery.sh ${APP_ROOT}/start_celery.sh

# Collect statics
RUN mkdir -p ${APP_ROOT}/eventol/static

# Create media folder
RUN mkdir -p ${APP_ROOT}/eventol/media

# Create log file
RUN touch /var/log/eventol/eventol.log

# Compile .po files
RUN sed -i 's@#~ @@g' ${APP_ROOT}/eventol/conf/locale/*/LC_MESSAGES/djangojs.po

EXPOSE 8000

VOLUME ${APP_ROOT}/eventol/media
VOLUME ${APP_ROOT}/eventol/static

CMD ["tail", "-f", "/dev/null"]
