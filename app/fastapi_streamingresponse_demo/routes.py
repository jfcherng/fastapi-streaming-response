# Core Library
import asyncio
from typing import cast
from pathlib import Path
from functools import lru_cache
from collections.abc import AsyncIterable

# Third party
from fastapi import Query, FastAPI, APIRouter
from fastapi.responses import RedirectResponse, StreamingResponse

# First party
from fastapi_streamingresponse_demo.llm import Llm, PromptData, GeneratedData


def register_ui_routes(app: FastAPI):
    @app.get("/health")
    async def health_check():
        return dict(status="alive")


def register_api_routes(router: APIRouter):
    @router.get("", summary="Redirect to Docs")
    async def root():
        return RedirectResponse(url="/docs")

    @router.get("/", summary="Redirect to Docs")
    async def root_():
        return RedirectResponse(url="/docs")

    @router.get("/health")
    async def health_check():
        return dict(status="alive")

    @router.post("/llm/blab", summary="Ask llm to blab")
    async def stream_response(
        prompt_data: PromptData,
        model_path: Path = Query(
            "/opt/app/model", title="Model path", description="Path to the model"
        ),
        max_tokens: int = Query(256, title="max_tokens", description="max_tokens", ge=32),
        temperature: float = Query(
            0.7, title="temperature", description="temperature", gt=0.0, le=1.0
        ),
    ):
        prompt_data.model_path = prompt_data.model_path or model_path
        prompt_data.max_tokens = prompt_data.max_tokens or max_tokens
        prompt_data.temperature = prompt_data.temperature or temperature
        return StreamingResponse(
            content=cast(AsyncIterable, blab_llm(prompt_data)), media_type="text/event-stream"
        )


async def blab_llm(prompt_data: PromptData):
    if str(prompt_data).startswith("~"):  # e.g., ~/Downloads/mistral-7B-v0.1
        prompt_data.model_path = prompt_data.expanduser()

    llm = get_llm()
    yield "[\n"
    seq_ = 0
    async for text in llm.generate(prompt_data):
        yield GeneratedData(generated_text=text, seq_=seq_, is_last_=False).model_dump_json()
        yield ",\n"
        await asyncio.sleep(0.05)
        seq_ += 1
    yield GeneratedData(generated_text="", seq_=seq_, is_last_=True).model_dump_json()
    yield "\n]\n"


@lru_cache
def get_llm():
    return Llm()
