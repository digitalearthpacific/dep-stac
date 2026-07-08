# This makefile is for populating a local DB

export PGHOST := localhost
export PGPORT := 5432
export PGUSER := username
export PGPASSWORD := password
export PGDATABASE := postgis

# export AWS_PROFILE=XXX # For get_upsert_items

up:
	docker compose up

shell:
	docker compose exec -it stac bash

# This happens locally (not within Docker container). Most other commands need DB connection etc. so they are run within the container.
create_collections:
	python3 create_collections.py --env staging
	python3 create_collections.py --env production

migrate:
	pypgstac migrate

enable_context_counts:
	docker compose exec postgis psql -U username -d postgis -c \
		"SET search_path TO pgstac, public; INSERT INTO pgstac_settings (name, value) VALUES ('context', 'auto') ON CONFLICT ON CONSTRAINT pgstac_settings_pkey DO UPDATE SET value = excluded.value;"

create_and_upsert_collections_staging:
	python3 create_collections.py --env staging
	cd collections/staging && \
	ls | xargs -L 1 uv run pypgstac load collections --method upsert

upsert_wofs:
	python3 get_upsert_items.py \
		--bucket "dep-public-staging" \
		--prefix "dep_ls_wofs/0-0-3"

upsert_mangroves:
	python3 get_upsert_items.py \
		--bucket "dep-public-staging" \
		--prefix "dep_s2_mangroves/0-3-0" \
		--collection-override "dep_s2_mangroves"

upsert_ls_geomad:
	python3 get_upsert_items.py \
		--bucket "dep-public-staging" \
		--prefix "dep_ls_geomad/0-3-0-test" \
		--collection-override "dep_ls_geomad"
