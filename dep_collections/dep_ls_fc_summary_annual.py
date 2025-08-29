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
dep_ls_fc_summary_annual = Collection(
    id="dep_ls_fc_summary_annual",
    description="Annual summaries of fractional cover",
    title="Fractional Cover Annual Summary",
    extent=dep_ls_fc_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "Vegetation", "Bare ground", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="Amazon",
            roles=["host"],
            url="https://aws.amazon.com",
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
                "name": "bs_pc_10",
                "common_name": "10th percentile of bare soil percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "bs_pc_50",
                "common_name": "50th percentile of bare soil percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "bs_pc_90",
                "common_name": "90th percentile of bare soil percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "pv_pc_10",
                "common_name": "10th percentile of photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "pv_pc_50",
                "common_name": "50th percentile of photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "bs_pc_90",
                "common_name": "90th percentile of photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "npv_pc_10",
                "common_name": "10th percentile of non-photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "npv_pc_50",
                "common_name": "50th percentile of non-photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "npv_pc_90",
                "common_name": "90th percentile of non-photosynthetic vegetation percentage",
                "description": "",
                "min": 0,
                "max": 127,
                "nodata": 255
              },
              {
                "name": "count_valid",
                "common_name": "Count of clear and valid observations",
                "description": "",
                "min": 0,
                "max": 32767
              },
              {
                "name": "qa",
                "common_name": "quality assurannce band",
                "description": "",
                "min": 0,
                "max": 2
              }
                ],
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
