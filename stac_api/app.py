import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import (
    JSONResponse, # type: ignore[reportPrivateImportUsage]
    create_get_request_model,
    create_post_request_model,
)
from stac_fastapi.extensions import (
    FieldsExtension,
    FilterExtension,
    QueryExtension,
    SortExtension,
    TokenPaginationExtension,
)
from stac_fastapi.pgstac.config import Settings
from stac_fastapi.pgstac.core import CoreCrudClient
from stac_fastapi.pgstac.db import close_db_connection, connect_to_db
from stac_fastapi.pgstac.types.search import PgstacSearch
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
post_request_model = create_post_request_model(extensions, base_model=PgstacSearch)
get_request_model = create_get_request_model(extensions)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to database on startup, close on shutdown."""
    await connect_to_db(app)
    yield
    await close_db_connection(app)


api = StacApi(
    app=FastAPI(
        title=title,
        description=description,
        lifespan=lifespan,
    ),
    title=title,
    description=description,
    extensions=extensions,
    settings=settings,
    client=CoreCrudClient(pgstac_search_model=post_request_model, landing_page_id=id),
    search_get_request_model=get_request_model,
    search_post_request_model=post_request_model,
    response_class=JSONResponse,
)

app: FastAPI = api.app

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)