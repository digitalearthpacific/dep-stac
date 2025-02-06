#!/usr/bin/env python3

from pathlib import Path

from dep_collections.dep_ls_geomad import dep_ls_geomad
from dep_collections.dep_ls_wofs_summary_annual import dep_ls_wofs_summary_annual
from dep_collections.dep_ls_wofl import dep_ls_wofl
from dep_collections.dep_s1_geomad import dep_s1_geomad
from dep_collections.dep_s2_geomad import dep_s2_geomad
from dep_collections.dep_s2_mangroves import dep_s2_mangroves
from dep_collections.dep_s2s1_mrd import dep_s2s1_mrd
from dep_collections.dep_s2ls_intertidal import dep_s2ls_intertidal

STAGING_URL = "https://stac.staging.digitalearthpacific.io"
OUT_FOLDER = "collections"

out_dir = Path(OUT_FOLDER)
out_dir.mkdir(exist_ok=True)

all_collections = (
    dep_ls_wofs_summary_annual,
    dep_ls_wofl,
    dep_ls_geomad,
    dep_s1_geomad,
    dep_s2_geomad,
    dep_s2_mangroves,
    dep_s2s1_mrd,
    dep_s2ls_intertidal
)

for collection in all_collections:
    collection_url = f"{STAGING_URL}/collections/{collection.id}"
    collection.validate()
    collection.set_self_href(collection_url)

    print(f"Writing {collection.id} to {out_dir}")
    collection_dict = collection.save_object(
        dest_href=out_dir / f"{collection.id}.json"
    )
