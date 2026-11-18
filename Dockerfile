FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /usr/local/bin/

# Used by dep-flux workflows (stac-collection-sync, stac-items-ingest), which run
# pypgstac, /code/get_upsert_items.py and read /code/collections/{staging,production}.
# postgresql-client: psql for ad hoc DB work
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/code/.venv/bin:$PATH"