from vnstock3 import Vnstock
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
import pandas as pd
from typing import Annotated
from langchain_core.messages import HumanMessage, AIMessage

from stock_buddy.functions.helper import invoke_agent_with_dataframe


@tool(parse_docstring=True, response_format="content_and_artifact")
def visualize_data(state: Annotated[dict, InjectedState]) -> str:
    """
    This function visualizes chart based on the user's query
    
    Args:


    Returns:
        str: The path to the path of chart image.
    """

    prefix_prompt = """
    Your task is to visualize the data in the DataFrame and save the chart as an image then return the image under base64.
    """

    print("*" * 100)
    last_answer = next((m for m in reversed(state['messages']) 
                        if isinstance(m, AIMessage) and not isinstance(m.artifact, str) and m.content != ""), 
                        None)
    df = next((m.artifact for m in reversed(state['messages']) if isinstance(m, AIMessage) and isinstance(m.artifact, pd.DataFrame)), None)
    
    try:
        img_path =  invoke_agent_with_dataframe(state, df, prefix=prefix_prompt)

        final_answer = f"### THE ANSWER IS: {last_answer.content}\n\n. ### THE IMAGE BASE54 IS: {img_path}"
        last_answer.content = final_answer
        return last_answer, img_path
    except Exception as e:
        return f"Error: {e}", None