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
dep_ls_wofs_summary_alltime = Collection(
    id="dep_ls_wofs_summary_alltime",
    description="WOfS all time (1984-2023) summary over the Pacific.",
    title="WOfS Landsat All-time Summary ",
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
                    "name": "count_clear",
                    "description": "Count of clear observations",
                    "min": 0,
                    "max": 32767,
                    "nodata": -999,
                },
                {
                    "name": "count_wet",
                    "description": "Count of observations that are water",
                    "min": 0,
                    "max": 32767,
                    "nodata": -999,
                },
                {
                    "name": "frequency",
                    "description": "Frequency of water observations",
                    "min": 0,
                    "max": 1,
                    "nodata": "nan",
                },
                {
                    "name": "frequency_masked",
                    "description": "Frequency of water observations, with ocean masked",
                    "min": 0,
                    "max": 1,
                    "nodata": "nan",
                },
            ],
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
