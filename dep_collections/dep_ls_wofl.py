from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

dep_ls_wofl_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_wofl = Collection(
    id="dep_ls_wofl",
    description="Water observations from space (WOfS) feature layers",
    title="WOfS feature layer",
    extent=dep_ls_wofl_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "WOfS", "WOFL", "Water", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="Amazon",
            roles=["host"],
            url="https://aws.amazon.com/",
        ),
        Provider(
            name="USGS",
            roles=["producer", "processor", "licensor"],
            url="https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products",
        ),
        Provider(name="NASA", roles=["licensor"], url="https://www.nasa.gov/"),
    ],
    summaries=Summaries(
        {
            "gsd": [30],
            "eo:bands": [
                {
                    "name": "water",
                    "common_name": "water",
                    "description": "Water feature layer for a single date and time",
                    "min": 0,
                    "max": 256,
                    "nodata": 1,
                },
            ],
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
