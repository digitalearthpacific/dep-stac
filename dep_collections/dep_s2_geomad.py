from datetime import datetime, timezone

from pystac import (
    Collection,
    Extent,
    Provider,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)

dep_s2_geomad_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(2017, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

S2_BANDS = [
    "B02",
    "B03",
    "B04",
    "B05",
    "B06",
    "B07",
    "B08",
    "B8A",
    "B11",
    "B12",
]
MAD_BANDS = [("emad", "Euclidean"), ("smad", "Spectral"), ("bcmad", "Bray-curtis")]

# Create a Collection
dep_s2_geomad = Collection(
    id="dep_s2_geomad",
    description="Sentinel-2 Geometric Median and Absolute Deviations (GeoMAD) over the Pacific.",
    title="Landsat GeoMAD",
    extent=dep_s2_geomad_extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-2", "GeoMAD", "Pacific"],
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
        ),
        Provider(name="Esri", roles=["processor"], url="https://www.esri.com/"),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                dict(
                    name=band,
                    common_name=band,
                    description=f"Median for {band} band",
                    min=0,
                    max=10_000,
                    nodata=0,
                )
                for band in S2_BANDS
            ]
            + [
                dict(
                    name=band[0],
                    common_name=f"{band[1]} MAD",
                    description=f"{band[1]} median absolute deviations across all bands",
                    min=0,
                    max=10_000,
                    nodata=0,
                )
                for band in MAD_BANDS
            ]
            + [
                dict(
                    name="count",
                    common_name="Count clear",
                    description="Count of clear observations",
                    min=0,
                    max=250,
                    nodata=0,
                )
            ],
            "platform": ["Sentinel-2A", "Sentinel-2B"],
        },
    ),
)
