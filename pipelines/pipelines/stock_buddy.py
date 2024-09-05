from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import os
import requests
from typing import Optional


class Pipeline:
    class Valves(BaseModel):
        OPENAI_API_KEY: str = ""

    def __init__(self):
        self.name = "OpenAI Pipeline"
        self.valves = self.Valves(
            **{
                "OPENAI_API_KEY": os.getenv()
            }
        )

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")


    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        OPENAI_API_KEY = self.valves.OPENAI_API_KEY

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        pass

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        pass
