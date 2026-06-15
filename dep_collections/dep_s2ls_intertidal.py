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
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_s2ls_intertidal = Collection(
    id="dep_s2ls_intertidal",
    description="This dataset provides spatial information on intertidal elevation and exposure across Pacific Island coastlines derived from multi-sensor satellite observations. It includes elevation estimates and exposure metrics indicating the proportion of time areas are exposed within the intertidal zone. The dataset supports coastal monitoring, habitat mapping, and shoreline dynamics analysis.\n\nLineage:\nProduced by combining Landsat and Sentinel observations to model intertidal elevation and calculate exposure metrics.\n\nProcessing level:\nModelled\n\nDataset type:\nModelled surface",
    title="Intertidal Elevation and Exposure (Sentinel-1/Sentinel-2/Landsat, 10 m)",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["intertidal", "elevation", "bathymetry"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "elevation",
                    "common_name": "Elevation",
                    "description": "Elevation In Metres",
                    "min": -0.8,
                    "max": 8.0,
                    "nodata": 255,
                },
                {
                    "name": "Exposure",
                    "common_name": "Exposure",
                    "description": "Intertidal Extent Exposure Percentage",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                },
            ],
            "platform": ["Sentinel-1", "Sentinel-2", "Landsat-7", "Landsat-8", "Landsat-9"],
        },
    ),
)


dep_s2ls_intertidal.add_link(
    Link(
        rel="wms",
        target=WMS_URL,
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["dep_s2ls_intertidal"],
            "wms:styles": ["Elevation", "Exposure"],
            "wms:dimensions": {},
        },
    )
)
