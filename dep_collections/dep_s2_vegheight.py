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
    SpatialExtent([[100, -30, 260, 30]]),
    TemporalExtent([[datetime(2012, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_s2_vegheight = Collection(
    id="dep_s2_vegheight",
    description="Vegetation height in the Pacific",
    title="Vegetation height in the Pacific from Sentinel-2",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-2", "Vegetation", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="ESA",
            roles=["producer", "licensor"],
            url="https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
        ),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "height",
                    "common_name": "height",
                    "description": "Height of vegetation",
                    "min": 0.0,
                    "max": 40.0,
                    "nodata": "nan",
                },
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B", "Sentinel-2C"],
        }
    ),
)
