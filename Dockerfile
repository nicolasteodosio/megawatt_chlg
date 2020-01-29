FROM python:3.6-alpine

RUN apk upgrade && \
  apk add --no-cache --virtual build-dependencies linux-headers postgresql-dev make gcc \
  g++ ca-certificates zlib-dev jpeg-dev tiff-dev freetype-dev lcms2-dev \
  libwebp-dev tcl-dev tk-dev libxml2-dev libxslt-dev git && \
  rm -rf /var/cache/apk/*

COPY . /opt/code
WORKDIR /opt/code
RUN pip install pipenv
RUN pipenv sync
RUN pipenv run python manage.py migrate