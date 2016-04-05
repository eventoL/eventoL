FROM python:2.7
MAINTAINER Federico Gonzalez

# Update debian packages
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y

# Install debian dependencies
RUN apt-get --force-yes install -y wget curl locales git nano htop build-essential nginx
RUN apt-get --force-yes install -y nodejs nodejs-legacy
RUN apt-get --force-yes install -y binutils libproj-dev gdal-bin libgeoip1 python-gdal
RUN apt-get --force-yes install -y libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev
RUN apt-get --force-yes install -y jpegoptim optipng
RUN apt-get --force-yes install -y libffi-dev libxml2-dev libxslt1-dev

# Install npm
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN wget http://npmjs.org/install.sh
RUN sh install.sh

# Configure npm
RUN npm config set registry http://registry.npmjs.org
RUN git config --global url."https://".insteadOf git://

# Install bower and gulp
RUN npm install -g bower

# Download source
RUN cd /var/www/ && git clone https://github.com/gnutn/eventoL.git eventol

# Install python dependencies
RUN cd /var/www/eventol/ && virtualenv venv
RUN cd /var/www/eventol/ && . venv/bin/activate && pip install -r requirements.txt

# Install npm and bower dependencies
RUN cd /var/www/eventol/ && bower install --allow-root

# Compile less files
RUN npm install -g less
RUN lessc /var/www/eventol/manager/static/manager/less/flisol.less > /var/www/eventol/manager/static/manager/css/flisol.css
RUN lessc /var/www/eventol/manager/static/manager/less/flisol-bootstrap.less > /var/www/eventol/manager/static/manager/css/flisol-bootstrap.css

# Configure source
RUN chmod +x /var/www/eventol/manage.py

# Install supervisord and gunicorn
RUN cd /var/www/eventol/ && . venv/bin/activate && pip install supervisor
RUN cd /var/www/eventol/ && . venv/bin/activate && pip install gunicorn
ADD supervisor/supervisord.conf /etc/supervisord.conf
ADD gunicorn/gunicorn-eventol.sh /var/www/eventol/gunicorn-eventol.sh
RUN chmod +x /var/www/eventol/gunicorn-eventol.sh

# Configure nginx
RUN rm -rf /etc/nginx/sites-enabled/*
RUN rm -rf /etc/nginx/sites-available/*
RUN rm -rf /etc/nginx/conf.d/default.conf
ADD nginx/nginx.conf /etc/nginx/nginx.conf
ADD nginx/eventol.conf /etc/nginx/sites-available/eventol.conf
RUN ln -s /etc/nginx/sites-available/eventol.conf /etc/nginx/sites-enabled/eventol.conf

# Add run script
RUN mkdir /var/www/eventol/log
ADD script/run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8000

CMD ["/run.sh"]