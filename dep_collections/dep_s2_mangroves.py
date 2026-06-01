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
                    "nodata": 255,
                }
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B"],
        },
    ),
)


dep_s2_mangroves.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["mangroves"],
            "wms:styles": ["style_mangroves", "style_mangroves_alt"],
            "wms:dimensions": {},
        },
    )
)
