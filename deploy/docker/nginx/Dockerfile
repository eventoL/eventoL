FROM nginx:latest

# Elimina el default si existe
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu archivo de configuración custom
COPY sites-enabled/eventol /etc/nginx/conf.d/eventol.conf
