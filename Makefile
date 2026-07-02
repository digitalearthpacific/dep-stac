# This makefile is for populating a local DB

up:
	docker compose up

shell:
	docker compose exec -it stac bash

# This happens locally (not within Docker container). Most other commands need DB connection etc. so they are run within the container.
create_collections:
	python3 create_collections.py --env staging
	python3 create_collections.py --env production

migrate:
	docker compose exec stac \
		pypgstac migrate

create_and_upsert_collections_staging:
	docker compose exec stac \
		bash -c " \
			python3 create_collections.py --env staging && \
			cd collections/staging && \
			ls | xargs -L 1 \
				pypgstac load collections --method upsert \
		"


# TODO: These don't have AWS credentials locally.
upsert_wofs:
	docker compose exec stac \
		python3 get_upsert_items.py \
			--bucket "output" \
			--prefix "dep_ls_wofs/0-0-3/"

upsert_mangroves:
	docker compose exec stac \
		python3 get_upsert_items.py \
			--bucket "output" \
			--prefix "dep_s2_mangroves/0-0-5/" \
			--collection-override "dep_s2_mangroves"
