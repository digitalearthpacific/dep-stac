FROM ghcr.io/osgeo/gdal:ubuntu-full-3.7.1

RUN apt-get update && apt-get install -y \
    # Python tools
    python3-pip \
    python3-dev \
    build-essential \
    # User tools
    git \
    fish \
    # Postgres libs
    postgresql-client \
    libpq-dev \
    # Certificates for some reason
    ca-certificates \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

ADD . /code

WORKDIR /code

# Don't use old pygeos
ENV USE_PYGEOS=0
