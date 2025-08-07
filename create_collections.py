#!/usr/bin/env python3

import typer

from pathlib import Path

from dep_collections.dep_ls_geomad import dep_ls_geomad
from dep_collections.dep_ls_wofs_summary_annual import dep_ls_wofs_summary_annual
from dep_collections.dep_ls_wofs_summary_alltime import dep_ls_wofs_summary_alltime
from dep_collections.dep_ls_wofl import dep_ls_wofl
from dep_collections.dep_ls_fc import dep_ls_fc
from dep_collections.dep_pdhhdx_population import dep_pdhhdx_population
from dep_collections.dep_s1_geomad import dep_s1_geomad
from dep_collections.dep_s2_geomad import dep_s2_geomad
from dep_collections.dep_s2_mangroves import dep_s2_mangroves
from dep_collections.dep_s2_sdb import dep_s2_sdb
from dep_collections.dep_s2s1_mrd import dep_s2s1_mrd
from dep_collections.dep_s2ls_intertidal import dep_s2ls_intertidal
from dep_collections.dep_s2_ocm import dep_s2_ocm

STAGING_URL = "https://stac.staging.digitalearthpacific.io"
PRODUCTION_URL = "https://stac.digitalearthpacific.org"
PROD_FOLDER = "collections/production"
STAGING_FOLDER = "collections/staging"

PRODUCTION_COLLECTIONS = (
    dep_ls_wofs_summary_annual,
    dep_ls_wofs_summary_alltime,
    dep_ls_wofl,
    dep_ls_geomad,
    dep_s1_geomad,
    dep_s2_geomad,
    dep_s2_mangroves,
    dep_s2_sdb,
    dep_s2s1_mrd,
    dep_s2ls_intertidal,
)

STAGING_COLLECTIONS = (
    dep_ls_wofs_summary_annual,
    dep_ls_wofs_summary_alltime,
    dep_ls_wofl,
    dep_ls_geomad,
    dep_ls_fc,
    dep_pdhhdx_population,
    dep_s1_geomad,
    dep_s2_geomad,
    dep_s2_mangroves,
    dep_s2_sdb,
    dep_s2s1_mrd,
    dep_s2ls_intertidal,
    dep_s2_ocm,
)


app = typer.Typer()


@app.command()
def render_collections(
    env: str = typer.Option(
        "staging", help="Environment to use: staging or production"
    ),
):
    is_prod = env == "production"

    if is_prod:
        base_url = PRODUCTION_URL
        all_collections = PRODUCTION_COLLECTIONS
    elif env == "staging":
        base_url = STAGING_URL
        all_collections = STAGING_COLLECTIONS
    else:
        raise ValueError("Invalid environment. Choose 'staging' or 'production'.")

    out_dir = Path(PROD_FOLDER) if is_prod else Path(STAGING_FOLDER)

    for collection in all_collections:
        collection_url = f"{base_url}/collections/{collection.id}"
        collection.validate()
        collection.set_self_href(collection_url)

        print(f"Writing {collection.id} to {out_dir}")
        _ = collection.save_object(dest_href=out_dir / f"{collection.id}.json")


if __name__ == "__main__":
    app()
