#!/usr/bin/env python3

import json
from multiprocessing.dummy import Pool as ThreadPool
from types import SimpleNamespace
from typing import Generator, Iterable

import click
import pystac

from odc.aws import s3_find

from odc.aws import s3_fetch
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item


def download_item(item: SimpleNamespace):
    url = item.url
    item_bin = s3_fetch(url)
    return Item.from_dict(json.loads(item_bin))


def download_items(s3_files: Generator) -> Iterable[Item]:
    pool = ThreadPool(20)
    items = pool.map(download_item, s3_files)
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
@click.option("--bucket", help="S3 Bucket")
@click.option("--prefix", help="Prefix", default=None)
@click.option(
    "--dump-items", help="Dump items to a file", type=bool, default=False, is_flag=True
)
@click.option(
    "--collection-override", help="Change the collection name", type=str, default=None
)
def get_insert_items(
    bucket: str, prefix: str | None, dump_items: bool, collection_override: str
):
    s3_files = s3_find(f"s3://{bucket}/{prefix}", glob="**/*.stac-item.json")
    items = download_items(s3_files)
    count = insert_items(items, collection_override, dump_items=dump_items)
    print(f"Found and updated {count} items in the database")


if __name__ == "__main__":
    get_insert_items()
