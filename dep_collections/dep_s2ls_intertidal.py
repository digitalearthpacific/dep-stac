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
dep_s2ls_intertidal = Collection(
    id="dep_s2ls_intertidal",
    description="Intertidal Elevation and Exposure for the Pacific Islands",
    title="Intertidal Elevation and Exposure",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-2", "Landsat", "Pacific"],
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
                    "name": "elevation",
                    "common_name": "Elevation",
                    "description": "Elevation In Metres",
                    "min": -0.8,
                    "max": 8.0,
                    "nodata": 255,
                },
                {
                    "name": "Exposure",
                    "common_name": "Exposure",
                    "description": "Intertidal Extent Exposure Percentage",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                },
            ],
            "platform": ["Sentinel-1", "Sentinel-2", "Landsat-7", "Landsat-8", "Landsat-9"],
        },
    ),
)
