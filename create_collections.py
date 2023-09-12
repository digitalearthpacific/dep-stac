#!/usr/bin/env python3

from pathlib import Path

from dep_collections.dep_ls_wofs import dep_ls_wofs
from dep_collections.dep_s2_mangroves import dep_s2_mangroves

STAGING_URL = "https://stac.staging.digitalearthpacific.org"
OUT_FOLDER = "collections"

out_dir = Path(OUT_FOLDER)
out_dir.mkdir(exist_ok=True)

all_collections = (dep_ls_wofs, dep_s2_mangroves)

for collection in all_collections:
    collection_url = f"{STAGING_URL}/collections/{collection.id}"
    collection.validate()
    collection.set_self_href(collection_url)

    print(f"Writing {collection.id} to {out_dir}")
    collection_dict = collection.save_object(dest_href=out_dir / f"{collection.id}.json")
