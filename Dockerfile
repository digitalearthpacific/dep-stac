FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    postgresql-client \
    libpq-dev \
    ca-certificates \
    libhdf5-dev \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

WORKDIR /code

# Install deps first for better layer caching
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000
ENV PATH="/code/.venv/bin:$PATH"

CMD uv run uvicorn stac_api.app:app --host ${APP_HOST} --port ${APP_PORT} --log-level info
