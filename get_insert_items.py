#!/usr/bin/env python3

import json

import click
import pystac
from dep_tools.azure import download_blobs, list_blob_container
from dep_tools.utils import get_container_client
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item


def insert_items(
    items: list, collection_override: str = None, dump_items: bool = False
) -> int:
    all_items = []

    for item_bytes in items:
        item = json.loads(item_bytes)
        if collection_override is not None:
            stac_item = Item.from_dict(item)
            stac_item.collection_id = collection_override
            stac_item.add_link(
                pystac.Link(
                    pystac.RelType.COLLECTION,
                    collection_override,
                    media_type=pystac.MediaType.JSON,
                )
            )
            item = stac_item.to_dict()

        all_items.append(item)

    if dump_items:
        with open("items.json", "w") as f:
            json.dump(all_items, f, indent=2)

    method = Methods.upsert
    db = PgstacDB()
    loader = Loader(db)
    loader.load_items(all_items, insert_mode=method)

    return len(all_items)


@click.command()
@click.option("--storage-container", help="Storage container")
@click.option("--prefix", help="Prefix")
@click.option(
    "--dump-items", help="Dump items to a file", type=bool, default=False, is_flag=True
)
@click.option(
    "--collection-override", help="Change the collection name", type=str, default=None
)
def get_insert_items(
    storage_container: str, prefix: str, dump_items: bool, collection_override: str
):
    container_client = get_container_client(container_name=storage_container)
    stac_urls = list_blob_container(container_client, prefix, suffix=".stac-item.json")
    items = download_blobs(container_client, stac_urls)
    count = insert_items(items, collection_override, dump_items=dump_items)
    print(f"Found and updated {count} items in the database")


if __name__ == "__main__":
    get_insert_items()
