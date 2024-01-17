from datetime import datetime, timezone

from pystac import (
    Collection,
    Extent,
    Provider,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)

dep_s1_mosaic_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

BANDS = ["vh", "vv", "vv_vh"]
S1_MOSAIC_BANDS = []

for band in BANDS:
    S1_MOSAIC_BANDS.append((f"mean_{band}", f"{band} Annual Mean"))
    S1_MOSAIC_BANDS.append((f"median_{band}", f"{band} Annual Median"))
    S1_MOSAIC_BANDS.append((f"std_{band}", f"{band} Annual Standard Deviation"))

# Create a Collection
dep_s1_mosaic = Collection(
    id="dep_s1_mosaic",
    description="Sentinel-1 mean and median annual mosaic.",
    title="Sentinel-1 Annual Mosaic",
    extent=dep_s1_mosaic_extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-1", "Pacific"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="Microsoft",
            roles=["host"],
            url="https://microsoft.com",
        ),
        Provider(
            name="ESA",
            roles=["producer", "licensor"],
            url="https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
        )
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                dict(
                    name=band[0],
                    common_name=band[1],
                    description=band[1],
                    min=0,
                    max=100,
                    nodata=-32767,
                )
                for band in S1_MOSAIC_BANDS
            ],
            "platform": ["Sentinel-1A", "Sentinel-1B"],
        },
    ),
)
