from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

dep_ls_fc_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_fc = Collection(
    id="dep_ls_fc",
    description="Scene-based fractional cover",
    title="Fractional cover",
    extent=dep_ls_fc_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "Vegetation", "Bare ground","Pacific"],
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
                    "name": "bs",
                    "common_name": "bare_soil",
                    "description": "Bare soil percentage",
                    "min": 0,
                    "max": 127,
                    "nodata": 255
                },
                {
                    "name": "pv",
                    "common_name": "photosynthetic_veg",
                    "description": "Photosynthetic (green) vegetation percentage",
                    "min": 0,
                    "max": 127,
                    "nodata": 255
                },
                {
                    "name": "npv",
                    "common_name": "non_photosynthetic_veg",
                    "description": "Non-photosynthetic (non-green) vegetation percentage",
                    "min": 0,
                    "max": 127,
                    "nodata": 255
                },
                {
                    "name": "ue",
                    "common_name": "unmixing_error",
                    "description": "Unmixing error",
                    "min": 0,
                    "max": 127,
                    "nodata": 255
                },
            ],
            "platform": ["landsat-4", "landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
