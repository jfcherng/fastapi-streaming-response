# Core Library
from typing import Annotated
from pathlib import Path
from collections.abc import AsyncGenerator

# Third party
from pydantic import Field, BaseModel


class PromptData(BaseModel):
    prompt: str
    model_path: Path = Path("/opt/app/model")
    max_tokens: Annotated[int, Field(gt=1, le=1024)] = 1024
    temperature: Annotated[float, Field(gt=0.0, le=1.0)] | None = None

    model_config = {"protected_namespaces": ()}


class GeneratedData(BaseModel):
    generated_text: str
    seq_: int
    is_last_: bool


class Llm:
    def __init__(self):
        ...

    async def generate(self, prompt_data: PromptData) -> AsyncGenerator[str, None]:
        text = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."""

        for word in prompt_data.prompt.split(" "):
            yield word

        for i, word in enumerate(text.split(" ")):
            yield f" {word}"
            if i >= prompt_data.max_tokens:
                break
