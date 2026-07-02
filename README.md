# DEP STAC

This repo contains configurations for a container to manage DEP's STAC documents.

## Set up for local dev

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Install dependencies

```bash
uv sync
source .venv/bin/activate
```

This creates a `.venv` and installs everything pinned in `uv.lock` Activate the venv.

### 2. Start the database and API

This runs postgis, and can either use the default stac-fastapi-pgstac image, or our custom app. Just change the image used in the [/docker-compose.yaml](./docker-compose.yaml).

```bash
make up
```

### 3. Run the pgstac schema migration

This is needed to structure the newly running, empty database.

```bash
make migrate
```

### 4. Optionally enable counts on search/list endpoints

This has performance implications.

```bash
make enable_context_counts
```


### 5. Generate and upsert staging collections

Generates collection JSON from [/dep_collections/staging](./dep_collections/staging)
and loads it into the database:

```bash
make create_and_upsert_collections_staging
```

### 6. Check it's running

Don't just check [http://0.0.0.0:8000](http://0.0.0.0:8000) because this works even before doing the `pypgstac migrate`. Check this:

```bash
curl [http://0.0.0.0:8000/collections](http://0.0.0.0:8000/collections)
```

Interactive docs are here: [localhost:8000/docs](http://localhost:8000/docs).

### Running tests

```bash
pytest tests/test_collections.py -v
```

### Stopping everything

```bash
docker compose down
```

Local data doesn't persist across restarts, so steps 3–4 need to be re-run after starting again. Add a volume to the `postgis` service in `docker-compose.yaml` if you want data to persist.


## Adding a new product

### 1. Create a collection

Create the collection in the [/dep_collections](./dep_collections) folder by copying one of the existing product's Python files.
Update all the fields as appropriate, ensuring it's accurately reflecting the data being
produced.

### 2. Add an entry for staging/production

Import the new collection in the [create_collections.py](create_collections.py) file and add the imported collection to the `STAGING_COLLECTIONS` and/or `PRODUCTION_COLLECTIONS` tuples to include it in that catalog.

### 3. Run the collection creation

Run the command `make create_collections` or `python create_collections.py` to make the new product's collection JSON.

### 4. Validate

```bash
pytest tests/test_collections.py -v
```

### 5. Create a pull request

Create a pull request in this repository. Get it reviewed. Once merged, run the appropriate Argo workflow. TODO: Document or link this Argo workflow.


### Collections

Regenerates collection JSON from `dep_collections/` and loads it into the database (upsert):
```bash
make create_and_upsert_collections_staging
```

### Items

Get all STAC Item JSONs from a S3 bucket/prefix, and write them to the DB. Look at `upsert_wofs` and `upsert_mangroves` in the [Makefile](Makefile) for examples.

You need S3 credentials to run this.

```bash
export AWS_PROFILE=XXX
export PGHOST=localhost
export PGPORT=5432
export PGUSER=username
export PGPASSWORD=password
export PGDATABASE=postgis
  python get_upsert_items.py \
    --bucket=my-bucket \
    --prefix=path/to/collection \
    --collection-override="collection_name"
```

You should see: "Found N items in the S3 bucket/prefix 'my-bucket/path/to/collection' and upserted them into the database". You can check this here: [http://0.0.0.0:8000/collections/collection_name/items](http://0.0.0.0:8000/collections/collection_name/items)

### Deleting Items for a Collection

```bash
psql -c "SET search_path TO pgstac,public; \
        DELETE FROM items WHERE collection=collection-id; \
        DELETE FROM collections WHERE id=collection-id;"
```


## Architecture: Dockerfile vs docker-compose

This repo has two container-related files that do different jobs:

- **`Dockerfile`: just the STAC API application itself.

- **`docker-compose.yaml`** orchestrates *local development only*: it
  spins up a throwaway PostGIS database alongside the API (built from the `Dockerfile` above), wires them together on a shared network, and exposes both on your machine.
  

### Deployment

In production, only the image built from the `Dockerfile` is deployed
(see `.github/workflows/build-test-docker.yml`, which builds and pushes that image to `ghcr.io` on every push to `main` and on releases. The database is a separately managed service.
