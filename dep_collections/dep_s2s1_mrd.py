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
dep_s2s1_mrd = Collection(
    id="dep_s2s1_mrd",
    description="Mineral resource detection in Fiji.",
    title="Mineral Resource Detection",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-1", "Sentinel-2", "Land-use/Land-cover", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "class",
                    "common_name": "classification",
                    "description": "Land use classification",
                    "min": 0,
                    "max": 8,
                    "nodata": 255,
                },
                {
                    "name": "proba",
                    "common_name": "probability",
                    "description": "Probability of land use classification",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                },
            ],
            "platform": ["Sentinel-1", "Sentinel-2", "esa-30m"],
        },
    ),
)
