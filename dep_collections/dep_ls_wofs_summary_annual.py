from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

dep_ls_wofs_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_wofs_summary_annual = Collection(
    id="dep_ls_wofs_summary_annual",
    description="WOfS Annual Summary over the Pacific.",
    title="WOfS Landsat Annual Summary ",
    extent=dep_ls_wofs_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "WOfS", "Water", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
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
                    "name": "mean",
                    "common_name": "water",
                    "description": "Mean annual water summary",
                    "min": 0,
                    "max": 100,
                    "nodata": -32767,
                },
            ],
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
