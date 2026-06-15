from pystac import (
    Link,
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone
from dep_collections.utils import WMS_URL

dep_ls_fc_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_fc = Collection(
    id="dep_ls_fc",
    description="This dataset provides scene-based fractional land cover derived from Landsat imagery, representing the percentage of bare soil, photosynthetic vegetation, and non-photosynthetic vegetation across the Pacific region. It is generated using multi-mission Landsat data at 30 m spatial resolution to support long-term environmental monitoring. The dataset enables applications such as land cover change analysis, ecosystem monitoring, and land degradation assessment.\n\nLineage: Derived from Landsat surface reflectance imagery using spectral unmixing to estimate fractional cover components per scene.\n\nProcessing level: Derived (scene-based)\n\nDataset type: Time-series (scene-based)",
    title="Fractional Land Cover, Scene-based (Landsat, 30 m)",
    extent=dep_ls_fc_extent,
    license="CC-BY-4.0",
    keywords=["fractional cover", "bare soil", "vegetation"],
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


dep_ls_fc.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["dep_ls_fc"],
            "wms:styles": ["fc_rgb_unmasked", "fc_rgb_masked"],
            "wms:dimensions": {},
        },
    )
)
