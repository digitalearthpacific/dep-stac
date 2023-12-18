#!/usr/bin/env python3

import json
from multiprocessing.dummy import Pool as ThreadPool
from typing import Iterable

import click
import pystac
from dep_tools.azure import list_blob_container
from dep_tools.utils import get_container_client
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item


def download_blob_item(blob: str):
    url = f"https://deppcpublicstorage.blob.core.windows.net/output/{blob}"
    return Item.from_file(url)


def download_blob_items(stac_urls: list[str]) -> Iterable[Item]:
    pool = ThreadPool(20)
    items = pool.map(download_blob_item, stac_urls)
    pool.close()
    pool.join()

    return items


def insert_items(
    items: Iterable[Item], collection_override: str = None, dump_items: bool = False
) -> int:
    all_items = []

    for item in items:
        if collection_override is not None:
            item.collection_id = collection_override
            item.add_link(
                pystac.Link(
                    pystac.RelType.COLLECTION,
                    collection_override,
                    media_type=pystac.MediaType.JSON,
                )
            )
            item = item.to_dict()

        all_items.append(item.to_dict())

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
    items = download_blob_items(stac_urls)
    count = insert_items(items, collection_override, dump_items=dump_items)
    print(f"Found and updated {count} items in the database")


if __name__ == "__main__":
    get_insert_items()
