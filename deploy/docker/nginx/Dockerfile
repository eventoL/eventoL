FROM nginx:alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config (use .conf extension for clarity)
COPY sites-enabled/eventol /etc/nginx/conf.d/eventol.conf
