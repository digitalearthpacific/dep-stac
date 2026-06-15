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

dep_ls_wofl_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_wofl = Collection(
    id="dep_ls_wofl",
    description="This dataset maps the presence of surface water across the Pacific region using Landsat satellite imagery. It identifies water bodies and captures temporal variability in water extent at the observation level. The dataset supports flood mapping, drought monitoring, and water resource analysis.\n\nLineage:\nDerived from Landsat imagery using water detection algorithms to classify surface water presence per scene.\n\nProcessing level:\nDerived (scene-based)\n\nDataset type:\nTime-series (scene-based)",
    title="Water Observations from Space (WOfS) Scene-based Surface Water (Landsat, 30 m)",
    extent=dep_ls_wofl_extent,
    license="CC-BY-4.0",
    keywords=["surface water", "water occurrence", "water frequency"],
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
                    "name": "water",
                    "common_name": "water",
                    "description": "Water feature layer for a single date and time",
                    "min": 0,
                    "max": 256,
                    "nodata": 1,
                },
            ],
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)


dep_ls_wofl.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["dep_ls_wofl"],
            "wms:styles": ["observations", "wet"],
            "wms:dimensions": {},
        },
    )
)
