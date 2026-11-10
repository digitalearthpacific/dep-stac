from pystac import (
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
    Provider,
    Summaries,
)
from datetime import datetime, timezone

extent = Extent(
    # The Fiji tiles produced, crossing the antimeridian (west > east, as STAC supports).
    SpatialExtent([[176.52, -21.74, -177.45, -11.78]]),
    # Annual, from the first year of Sentinel-1 and Sentinel-2 geomads; open-ended as new years are added.
    TemporalExtent([[datetime(2017, 1, 1, 0, 0, 0, 0, timezone.utc), None]]),
)

# Create a Collection
dep_s2s1_mrd = Collection(
    id="dep_s2s1_mrd",
    description="This dataset maps annual land cover across Fiji to support Mineral Resource Detection (MRD): finding and monitoring mineral resources such as quarries. Each 10 m pixel is classified as bare land, forest, crops, grassland, settlements, mangroves, water or quarry, with the probability of the predicted class.\n\nLineage:\nA random forest trained on labelled points from 2022, using Digital Earth Pacific Sentinel-2 and Sentinel-1 annual geomedians, spectral indices, and Copernicus DEM elevation and terrain. Where Sentinel-1 isn't available for a tile and year, the classification is made without it and the item lists it in mrd:missing_inputs.\n\nProcessing level:\nThematic Classification\n\nDataset type:\nCategorical map",
    title="Mineral Resource Detection Land Cover (Sentinel-1/Sentinel-2, 10 m)",
    extent=extent,
    license="CC-BY-4.0",
    keywords=["Sentinel-1", "Sentinel-2", "land cover", "quarry", "mineral resources", "Fiji"],
    providers=[
        Provider(
            name="Digital Earth Pacific",
            roles=["processor", "host"],
            url="https://digitalearthpacific.org",
        ),
        Provider(
            name="ESA",
            roles=["producer", "licensor"],
            url="https://sentinel.esa.int",
        ),
    ],
    summaries=Summaries(
        {
            "gsd": [10],
            "eo:bands": [
                {
                    "name": "class",
                    "common_name": "classification",
                    "description": "Land cover class: 1 bare land, 2 forest, 3 crops, 4 grassland, 5 settlements, 6 mangroves, 7 water, 8 quarry",
                    "min": 1,
                    "max": 8,
                    "nodata": 255,
                },
                {
                    "name": "proba",
                    "common_name": "probability",
                    "description": "Probability of the predicted class, in percent",
                    "min": 0,
                    "max": 100,
                    "nodata": 255,
                },
            ],
            "platform": ["Sentinel-1", "Sentinel-2", "Copernicus DEM GLO-30"],
        },
    ),
)
