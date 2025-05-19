from datetime import datetime, timezone

from pystac import (
    Collection,
    Extent,
    Provider,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)

dep_s2_ocm_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

dep_s2_ocm = Collection(
    id="dep_s2_ocm",
    description="Cloud masks for Sentinel-2 produced by Omnicloudmask",
    title="Sentinel-2 Omnicloudmask",
    extent=dep_s2_ocm_extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-2", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="Element-84",
            roles=["processor", "host"],
            url="https://www.element84.com",
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
                dict(
                    name="mask",
                    common_name="mask",
                    description=f"Cloud mask",
                    min=0,
                    max=3,
                    nodata=0,
                )
            ],
        }
    ),
)
