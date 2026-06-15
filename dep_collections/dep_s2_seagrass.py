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
dep_s2_seagrass = Collection(
    id="dep_s2_seagrass",
    description="This dataset maps the distribution of seagrass ecosystems across the Pacific region using Sentinel-2 imagery. It applies machine learning techniques to classify seagrass extent at high spatial resolution. The dataset supports marine habitat mapping, biodiversity monitoring, and coastal ecosystem management.\n\nLineage:\nDerived from Sentinel-2 imagery using machine learning models trained to classify seagrass extent.\n\nProcessing level:\nModelled\n\nDataset type:\nCategorical map",
    title="Seagrass Extent, Machine Learning (Sentinel-2, 10 m)",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["seagrass", "marine habitat", "ecosystem"],
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
                    "name": "seagrass",
                    "common_name": "seagrass",
                    "description": "Extent of seagrass",
                    "min": 0,
                    "max": 1,
                    "nodata": 255,
                },
                {
                    "name": "classification",
                    "common_name": "classification",
                    "description": "Result from the random forest coastal classification",
                    "min": 0,
                    "max": 16,
                    "nodata": 255,
                },
                {
                    "name": "seagrass_probability",
                    "common_name": "seagrass_probability",
                    "description": "Probability of seagrass presence",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                },
                {
                    "name": "seagrass_threshold_60",
                    "common_name": "seagrass_threshold_60",
                    "description": "Seagrass presence threshold (60%) from the probability",
                    "min": 0,
                    "max": 1,
                    "nodata": 255,
                },
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B", "Sentinel-2C"],
        }
    ),
)


dep_s2_seagrass.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["dep_s2_seagrass"],
            "wms:styles": ["seagrass", "probability", "classification", "seagrass_60"],
            "wms:dimensions": {},
        },
    )
)
