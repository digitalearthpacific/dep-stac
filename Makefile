# This makefile is for populating a local DB

up:
	docker-compose up

shell:
	docker-compose exec -it stac fish

create_collections:
	python3 create_collections.py

migrate:
	docker-compose exec stac \
		pypgstac migrate

insert_collections:
	docker-compose exec stac \
		bash -c " \
			python3 create_collections.py && \
			cd collections && \
			ls | xargs -L 1 \
				pypgstac load collections --method upsert \
		"

insert_wofs:
	docker-compose exec stac \
		python3 get_insert_items.py \
			--storage-container "output" \
			--prefix "dep_ls_wofs/0-0-3/"

insert_mangroves:
	docker-compose exec stac \
		python3 get_insert_items.py \
			--storage-container "output" \
			--prefix "dep_s2_mangroves/0-0-5/" \
			--collection-override "dep_s2_mangroves"
