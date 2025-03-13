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
dep_s2_sdb = Collection(
    id="dep_s2_sdb",
    description="Satellite-derived Bathymetry in the Pacific",
    title="Satellite-derived Bathymetry",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-2", "Bathymetry", "Pacific"],
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
                    "name": "depth",
                    "common_name": "depth",
                    "description": "Mean of the estimated depth of water, masked by a count of the number of times it was estimated",
                    "min": 0,
                    "max": 2,
                    "nodata": -32767,
                },
                {
                    "name": "mean",
                    "common_name": "mean",
                    "description": "Mean of the depth of water estimated",
                    "min": 0,
                    "max": 2,
                    "nodata": -32767,
                },
                {
                    "name": "stdev",
                    "common_name": "stdev",
                    "description": "Standard deviation of the depth of water",
                    "min": 0,
                    "max": 2,
                    "nodata": -32767,
                },
                {
                    "name": "count",
                    "common_name": "count",
                    "description": "Count of the number of times the depth was estimated",
                    "min": 0,
                    "max": 2,
                    "nodata": -32767,
                },
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B", "Sentinel-2C"],
        }
    ),
)
