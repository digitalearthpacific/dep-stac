from datetime import datetime, timezone

from pystac import (
    Link,
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
    description="This dataset provides annual coastline positions across the Pacific region derived from Landsat satellite imagery. It captures long-term shoreline change by mapping coastal boundaries over time. The dataset supports coastal change analysis, erosion monitoring, and climate adaptation planning.\n\nLineage:\nDerived from Landsat imagery by extracting and compositing annual shoreline vectors.\n\nProcessing level:\nFeature Extraction\n\nDataset type:\nVector time series",
    title="Annual Shorelines (Landsat, 30 m)",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["coastline", "shoreline", "coastal change"],
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

dep_ls_coastlines.add_link(
    Link(
        rel="wmts",
        target="https://tileserver.prod.digitalearthpacific.io/styles/coastlines/wmts.xml",
        media_type="application/xml",
        title="WMTS Service for this Collection",
        extra_fields={
            "wms:layers": ["coastlines-256", "coastlines-512"],
        }
    )
)
