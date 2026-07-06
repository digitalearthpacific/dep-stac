"""Validate all STAC collections defined in dep_collections."""

import importlib
import inspect
import pkgutil

import pystac
import pytest

import dep_collections


def discover_collections() -> list[tuple[str, pystac.Collection]]:
    """Discover all pystac.Collection instances in dep_collections local folder."""
    collections = []
    for _, modname, _ in pkgutil.iter_modules(
        dep_collections.__path__, dep_collections.__name__ + "."
    ):
        mod = importlib.import_module(modname)
        for name, obj in inspect.getmembers(mod):
            if isinstance(obj, pystac.Collection):
                collections.append((f"{modname}.{name}", obj))
    return collections


COLLECTIONS = discover_collections()


@pytest.mark.parametrize(
    "collection",
    [c for _, c in COLLECTIONS],
    ids=[name for name, _ in COLLECTIONS],
)
def test_collection_validates(collection: pystac.Collection):
    """Each collection should pass STAC schema validation."""
    collection.validate()
