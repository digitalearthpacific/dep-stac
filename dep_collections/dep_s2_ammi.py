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
dep_s2_ammi = Collection(
    id="dep_s2_ammi",
    description="Mangroves Extent over the Pacific using the Automatic Mangrove Map and Index (AMMI) ",
    title="Mangroves Extent (AMMI)",
    extent=extent,
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
                    "description": "Mangrove percentage",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                }
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B"],
        },
    ),
)
