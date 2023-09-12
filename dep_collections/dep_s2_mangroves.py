from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

dep_s2_mangroves_extent = Extent(
    SpatialExtent([[100, -30, 260, 30]]),
    TemporalExtent([[datetime(2012, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_s2_mangroves = Collection(
    id="dep_s2_mangroves",
    description="Mangroves Extent over the Pacific.",
    title="Mangroves Extent",
    extent=dep_s2_mangroves_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "Mangroves", "GMW", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="Microsoft",
            roles=["host"],
            url="https://microsoft.com",
        ),
        Provider(
            name="ESA",
            roles=["producer", "licensor"],
            url="https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
        ),
        Provider(name="Esri", roles=["processor"], url="https://www.esri.com/"),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "closed",
                    "common_name": "closed",
                    "description": "Closed mangrove cover",
                    "min": 0,
                    "max": 10000,
                    "nodata": -32767,
                },
                {
                    "name": "mangroves",
                    "common_name": "mangroves",
                    "description": "Mangrove cover",
                    "min": 0,
                    "max": 10000,
                    "nodata": -32767,
                },
                {
                    "name": "ndvi",
                    "common_name": "ndvi",
                    "description": "Normalised difference vegetation index",
                    "min": -1,
                    "max": 1,
                    "nodata": -32767,
                },
                {
                    "name": "regular",
                    "common_name": "regular",
                    "description": "Regular mangrove cover",
                    "min": 0,
                    "max": 1,
                    "nodata": -32767,
                },
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B"],
        },
    ),
)
