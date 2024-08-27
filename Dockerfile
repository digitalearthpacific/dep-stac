FROM ghcr.io/osgeo/gdal:ubuntu-full-3.8.5

RUN apt-get update && apt-get install -y \
    # Python  and build tools
    python3-pip \
    python3-dev \
    build-essential \
    gcc \
    # User tools
    git \
    fish \
    # Postgres libs
    postgresql-client \
    libpq-dev \
    # Certificates for some reason
    ca-certificates \
    # hdf5
    libhdf5-dev \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

RUN pip install --upgrade pip setuptools

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

# Don't use old pygeos
ENV USE_PYGEOS=0

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

# uvicorn stac_api.app:app --host ${APP_HOST} --port ${APP_PORT} --log-level info
CMD uvicorn stac_api.app:app --host ${APP_HOST} --port ${APP_PORT} --log-level info
