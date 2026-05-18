from datetime import datetime, timezone

from pystac import (
    Collection,
    Extent,
    Provider,
    SpatialExtent,
    TemporalExtent,
    Asset,
    MediaType,
)

extent = Extent(
    SpatialExtent([[-180, -90, 180, 90]]),
    TemporalExtent([[datetime(1980, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_ls_coastlines = Collection(
    id="dep_ls_coastlines",
    description="Annual coastline data derived from Landsat imagery.",
    title="Landsat Coastlines",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Landsat", "Coastlines", "Pacific"],
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
    assets={
        "geopackage": Asset(
            href="https://s3.us-west-2.amazonaws.com/dep-public-data/dep_ls_coastlines/dep_ls_coastlines_0-7-0-55.gpkg",
            title="Landsat Coastlines Geopackage",
            description="Geopackage containing annual coastline data derived from Landsat imagery.",
            roles=["data"],
            media_type=MediaType.GEOPACKAGE,
        ),
        "pmtiles": Asset(
            href="https://s3.us-west-2.amazonaws.com/dep-public-data/dep_ls_coastlines/dep_ls_coastlines_0-7-0-55.pmtiles",
            title="Landsat Coastlines PMTiles",
            description="PMTiles file containing annual coastline data derived from Landsat imagery.",
            roles=["data"],
            media_type="application/vnd.pmtiles",
        ),
    },
)
