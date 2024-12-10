ARG NGINX_VERSION=latest
ARG PORT=80

FROM nginx:${NGINX_VERSION}

# Supprime la configuration par défaut
RUN rm /etc/nginx/conf.d/default.conf

RUN apt-get update && \
    apt-get install -y bash

COPY ./nginx/nginx.conf /etc/nginx/conf.d/

EXPOSE ${PORT}
