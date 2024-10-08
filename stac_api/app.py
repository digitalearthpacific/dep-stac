import os

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import create_get_request_model, create_post_request_model
from stac_fastapi.extensions.core import (
    FieldsExtension,
    FilterExtension,
    QueryExtension,
    SortExtension,
    TokenPaginationExtension,
)
from stac_fastapi.pgstac.config import Settings
from stac_fastapi.pgstac.core import CoreCrudClient
from stac_fastapi.pgstac.db import close_db_connection, connect_to_db
from starlette.middleware.cors import CORSMiddleware

ENVIRONMENT = os.environ.get("ENVIRONMENT", "staging")

id = "dep-stac"
title = "Digital Earth Pacific STAC API"
description = "A SpatioTemporal Asset Catalog (STAC) API for Digital Earth Pacific"
if ENVIRONMENT != "production":
    id = id + f"-{ENVIRONMENT.lower()}"
    title = title + f" ({ENVIRONMENT})"
    description = description + f" ({ENVIRONMENT})"

settings = Settings()

extensions = [
    FilterExtension(),
    QueryExtension(),
    SortExtension(),
    FieldsExtension(),
    TokenPaginationExtension(),
]
post_request_model = create_post_request_model(extensions)
get_request_model = create_get_request_model(extensions)

api = StacApi(
    title=title,
    description=description,
    extensions=extensions,
    settings=settings,
    client=CoreCrudClient(post_request_model=post_request_model, landing_page_id=id),
    search_get_request_model=get_request_model,
    search_post_request_model=post_request_model,
    response_class=ORJSONResponse,
)

app: FastAPI = api.app

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Connect to database on startup."""
    await connect_to_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection."""
    await close_db_connection(app)
