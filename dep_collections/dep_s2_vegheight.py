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

extent = Extent(
    SpatialExtent([[100, -30, 260, 30]]),
    TemporalExtent([[datetime(2012, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_s2_vegheight = Collection(
    id="dep_s2_vegheight",
    description="This dataset provides spatial estimates of vegetation height across the Pacific region derived from Sentinel-2 imagery. It enables quartely analysis of forest structure, biomass, and ecosystem condition. The dataset supports applications in land management, carbon monitoring, and biodiversity assessment.\n\nLineage:\nDerived from Sentinel-2 imagery using modelling approaches to estimate vegetation canopy height.\n\nProcessing level:\nModelled\n\nDataset type:\nModelled surface",
    title="Vegetation Height, Satellite-Derived Canopy Height (Sentinel-2, 10 m)",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["canopy height", "forest structure", "vegetation"],
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
                    "name": "height",
                    "common_name": "height",
                    "description": "Height of vegetation",
                    "min": 0.0,
                    "max": 40.0,
                    "nodata": "nan",
                },
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B", "Sentinel-2C"],
        }
    ),
)


dep_s2_vegheight.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["dep_s2_vegheight"],
            "wms:styles": ["height", "confidence"],
            "wms:dimensions": {},
        },
    )
)
