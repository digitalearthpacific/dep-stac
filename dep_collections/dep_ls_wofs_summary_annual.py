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

dep_ls_wofs_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_wofs_summary_annual = Collection(
    id="dep_ls_wofs_summary_annual",
    description="WOfS annual summary over the Pacific.",
    title="WOfS Landsat Annual Summary ",
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


dep_ls_wofs_summary_annual.add_link(
    Link(
        rel="wms",
        target="https://ows.prod.digitalearthpacific.io/",
        media_type="application/vnd.ogc.wms_xml",
        title="WMS Service for this Collection",
        extra_fields={
            "wms:layers": ["wofs_ls_summary_annual"],
            "wms:styles": ["legacy_wofs_summary_annual_frequency_masked", "wofs_summary_annual_frequency_masked", "legacy_wofs_summary_annual_frequency", "wofs_summary_annual_frequency", "wofs_summary_annual_wet", "wofs_summary_annual_clear"],
            "wms:dimensions": {},
        },
    )
)
