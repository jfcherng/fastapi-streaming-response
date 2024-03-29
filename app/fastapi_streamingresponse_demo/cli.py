# Core Library
import logging
from pathlib import Path

# Third party
import click
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

# First party
from fastapi_streamingresponse_demo.routes import register_ui_routes, register_api_routes

_fallback_port = 8000

logger = logging.getLogger(__name__)


@click.group(help=__doc__)
def main():
    ...


@main.command()
@click.option("--port", type=int, default=_fallback_port, help="Port number")
def start_service(port: int):
    ui = FastAPI(
        title="StreamingResponse demo",
        version="v0.1.0",
        openapi_tags=[
            dict(name="StreamingResponse demo", description="FastAPI StreamingResponse demo")
        ],
        servers=[dict(url="/", description="Default server")],
    )
    api_router = APIRouter(prefix="/api", tags=["api"])
    register_api_routes(router=api_router)
    ui.include_router(router=api_router)

    register_ui_routes(ui)
    ui.mount("/", StaticFiles(directory=Path(__file__).parent / "ui", html=True), name="html+js")

    uvicorn.run(ui, host="localhost", port=port)


if __name__ == "__main__":
    start_service()
