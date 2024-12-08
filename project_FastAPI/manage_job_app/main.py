"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.exception_handlers import http_exception_handler

from manage_job_app.api.routers.offer import router as offer_router
from manage_job_app.api.routers.user import router as user_router
from manage_job_app.api.routers.application import router as application_router
from manage_job_app.container import Container
from manage_job_app.db import database
from manage_job_app.db import init_db


container = Container()
container.wire(modules=[
    "manage_job_app.api.routers.offer",
    "manage_job_app.api.routers.user",
    "manage_job_app.api.routers.application",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(offer_router, prefix="/offer")
app.include_router(user_router, prefix="/user")
app.include_router(application_router, prefix="/application")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
