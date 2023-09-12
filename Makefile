# This makefile is for populating a local DB

render_collections:
	python3 create_collections.py

insert_collections:
	cd collections && \
	ls | xargs -L 1 \
		pypgstac load collections \
			--dsn "postgres://username:password@localhost:5439/postgis" \
			--method upsert

insert_wofs:
	PGPASSWORD=password \
	PGUSER=username \
	PGPORT=5439 \
	PGHOST=localhost \
	PGDATABASE=postgis \
	python3 get_insert_items.py \
		--storage-container "output" \
		--prefix "dep_ls_wofs/0-0-3/"

insert_mangroves:
	PGPASSWORD=password \
	PGUSER=username \
	PGPORT=5439 \
	PGHOST=localhost \
	PGDATABASE=postgis \
	python3 get_insert_items.py \
		--storage-container "output" \
		--prefix "dep_s2_mangroves/0-0-2/" \
		--collection-override "dep_s2_mangroves"
