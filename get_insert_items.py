#!/usr/bin/env python3

import concurrent.futures
import json
from typing import Generator, Iterable

import click
import pystac
import s3fs
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item


def download_items(s3: s3fs.S3FileSystem, s3_files: Generator) -> Iterable[Item]:
    def fetch_item(s3_file):
        return Item.from_dict(json.loads(s3.read_text(s3_file)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        items = list(executor.map(fetch_item, s3_files))

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
    s3 = s3fs.S3FileSystem(anon=False)
    s3_files = s3.glob(f"s3://{bucket}/{prefix}/**/*.stac-item.json")

    items = download_items(s3, s3_files)
    count = insert_items(items, collection_override, dump_items=dump_items)
    print(f"Found and updated {count} items in the database")


if __name__ == "__main__":
    get_insert_items()
