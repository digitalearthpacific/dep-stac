from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_pdhhdx_population = Collection(
    id="dep_pdhhdx_population",
    description="Population density",
    title="Population density",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Population"],
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
            name="WorldPop",
            roles=["producer", "processor", "licensor"],
            url="https://www.worldpop.org/",
        ),
        Provider(
            name="Pacific Data Hub",
            roles=["producer", "processor", "licensor"],
            url="https://pacificdata.org/",
        ),
    ],
    summaries=Summaries(
        {
            "gsd": [100],
            "eo:bands": [
                {
                    "name": "pop_per_sqkm",
                    "common_name": "pop_per_sqkm",
                    "description": "Population per square kilometer",
                    "min": 0,
                    "max": 200000,
                    "nodata": "nan",
                },
            ],
        },
    ),
)
