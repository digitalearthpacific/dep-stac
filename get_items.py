#!/usr/bin/env python3

import json
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

import click
import pystac
from azure.storage.blob import ContainerClient
from dep_tools.utils import get_container_client
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item


def download_blob(container_client: ContainerClient, file: str):
    blob_client = container_client.get_blob_client(file)
    return blob_client.download_blob().readall()


def download_items(
    container_client: ContainerClient, items: list[str], n_workers: int = 20
) -> list:
    pool = ThreadPool(n_workers)
    stac_items = pool.map(partial(download_blob, container_client), items)
    pool.close()
    pool.join()
    return stac_items


def insert_items(items: list, out_file: str, collection_override: str = None) -> int:
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

    method = Methods.upsert
    db = PgstacDB()
    loader = Loader(db)
    loader.load_items(all_items, insert_mode=method)

    return len(all_items)


def list_stac_documents(container_client: ContainerClient, prefix: str) -> list:
    for blob_record in container_client.list_blobs(name_starts_with=prefix):
        blob_name = blob_record["name"]
        if blob_name.endswith(".stac-item.json"):
            yield blob_name


@click.command()
@click.option("--storage-container", help="Storage container")
@click.option("--prefix", help="Prefix")
@click.option(
    "--collection-override", help="Change the collection name", type=click.Path()
)
def get_items_for_product(
    storage_container: str, prefix: str, out_file: str, collection_override: str
):
    container_client = get_container_client(container_name=storage_container)
    stac_urls = list_stac_documents(container_client, prefix)
    items = download_items(container_client, stac_urls)
    count = insert_items(items, out_file, collection_override)
    print(f"Found and update {count} items in the database")


if __name__ == "__main__":
    get_items_for_product()
