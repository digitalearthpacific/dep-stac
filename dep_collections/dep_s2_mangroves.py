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
    keywords=["Sentinel-2", "Mangroves", "GMW", "Pacific"],
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
        Provider(
            name="Element-84",
            roles=["processor", "host"],
            url="https://www.element84.com",
        )
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "mangroves",
                    "common_name": "mangroves",
                    "description": "Mangrove cover",
                    "min": 0,
                    "max": 2,
                    "nodata": -32767,
                }
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B"],
        },
    ),
)
