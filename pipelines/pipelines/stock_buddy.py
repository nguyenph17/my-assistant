from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import os
import requests
from typing import Optional
import sys
from langchain_openai import ChatOpenAI

sys.path.append(os.getcwd())
from stock_buddy.graph import financial_chain


def generate_title(user_message: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini")
    title = llm.invoke(user_message)
    return title.content



class Pipeline:
    class Valves(BaseModel):
        OPENAI_API_KEY: str = ""

    def __init__(self):
        self.name = "Stock Buddy"
        self.valves = self.Valves(
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
        print(messages)
        if "Create a concise, 3-5 word phrase with an emoji as a title for the previous query." in user_message:
            title = generate_title(user_message)
            return title
        OPENAI_API_KEY = self.valves.OPENAI_API_KEY
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        answer = financial_chain.invoke(user_message, {"recursion_limit": 10})
        
        print(f"############ final answer: {answer}")
        return answer['messages'][-1].content