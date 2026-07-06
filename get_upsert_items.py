#!/usr/bin/env python3

import concurrent.futures
import json
from typing import Generator, Iterable, Optional

import pystac
import s3fs
import typer
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Item

app = typer.Typer()


def download_items(s3: s3fs.S3FileSystem, s3_files: Generator) -> Iterable[Item]:
    """Fetches item JSON documents from S3 in parallel"""

    def fetch_item(s3_file) -> Item:
        """ Fetches a single item JSON from S3 and returns a pystac.Item """
        return Item.from_dict(json.loads(s3.read_text(s3_file)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        items = list(executor.map(fetch_item, s3_files))

    return items


def upsert_items(
    items: Iterable[Item], collection_override: str | None = None, dump_items: bool = False
) -> int:
    """ Upserts (formatted) items into the database, optionally overriding the collection ID and dumping to a file. Returns the number of items upserted. """
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


@app.command()
def get_upsert_items(
    bucket: str = typer.Option(..., help="S3 Bucket to search for STAC items"),
    prefix: Optional[str] = typer.Option(None, help="Prefix to search for STAC items in the S3 bucket"),
    dump_items: bool = typer.Option(False, "--dump-items", help="Dump items to a JSON file"),
    collection_override: Optional[str] = typer.Option(
        None, help="Optional override to change the collection name"
    ),
):
    """ Fetches STAC items from S3 and upserts them into the database. """
    s3 = s3fs.S3FileSystem(anon=False)
    s3_files = s3.glob(f"s3://{bucket}/{prefix}/**/*.stac-item.json")

    items = download_items(s3, s3_files)
    count = upsert_items(items, collection_override, dump_items=dump_items)
    print(f"Found {count} items in the S3 bucket/prefix '{bucket}/{prefix}' and upserted them into the database")


if __name__ == "__main__":
    app()
