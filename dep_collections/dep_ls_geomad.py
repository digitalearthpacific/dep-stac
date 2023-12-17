from datetime import datetime, timezone

from pystac import (
    Collection,
    Extent,
    Provider,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)

dep_ls_geomad_extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

LS_BANDS = ['red', 'green', 'blue', 'nir08', 'swir16', 'swir22']
MAD_BANDS = [('emad', 'Euclidean'), ('smad', 'Spectral'), ('bcmad', "Bray-curtis")]

# Create a Collection
dep_ls_geomad = Collection(
    id="dep_ls_geomad",
    description="Landsat Geometric Median and Absolute Deviations (GeoMAD) over the Pacific.",
    title="Landsat GeoMAD",
    extent=dep_ls_geomad_extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "GeoMAD", "Pacific"],
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
                dict(
                    name=band,
                    common_name=band,
                    description=f"Median for {band} band",
                    min=0,
                    max=10_000,
                    nodata=0,
                ) for band in LS_BANDS
            ] + [
                dict(
                    name=band[0],
                    common_name=f"{band[1]} MAD",
                    description=f"{band[1]} median absolute deviations across all bands",
                    min=0,
                    max=10_000,
                    nodata=0,
                ) for band in MAD_BANDS
            ] +
            [
                dict(
                    name="count",
                    common_name="Count clear",
                    description="Count of clear observations",
                    min=0,
                    max=10_000,
                    nodata=0,
                )
            ]
            ,
            "platform": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"],
        },
    ),
)
