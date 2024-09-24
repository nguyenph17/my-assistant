import os
import sys
from typing import Annotated, TypedDict, List
import functools
import operator
import pandas as pd

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import END, StateGraph, START
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.prebuilt import create_react_agent

from stock_buddy.utils import get_current_datetime
from stock_buddy.functions.finance import balance_sheet, income_statement, cash_flow, ratio



def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [AIMessage(content=result["messages"][-1].content, name=name)]}

def create_team_supervisor(llm: ChatOpenAI, system_prompt, members) -> str:
    """An LLM-based router."""
    options = ["FINISH"] + members
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), team_members=", ".join(members))
    return (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )


# Document writing team graph state
class StockAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: str
    next: str
    df: pd.DataFrame

llm = ChatOpenAI(model="gpt-4o-mini")
tavily_tool = TavilySearchResults(max_results=3)

current_datetime_agent = create_react_agent(llm, 
                                            tools=[get_current_datetime], 
                                            state_modifier="Your task is to provide the time context for the conversation, you don't need to answer. You only use the function get_current_datetime if user mentions a relative time (year, month, day). Your answer must follow the format: 'The current date and time is current_date_time'.")
current_datetime_node = functools.partial(agent_node, 
                                          agent=current_datetime_agent, 
                                          name="CurrentDateTime")

check_stock_code_agent = create_react_agent(llm, 
                                            tools=[tavily_tool], 
                                            state_modifier="Your task is to provide the ticker symbol to the context for the conversation if there is only company name and no ticker symbol in the conversation. Your answer must follow the format: 'The ticker symbol of XXXXXXX is YYY'.")
check_stock_code_node = functools.partial(agent_node, agent=check_stock_code_agent, name="TickerSymbol")

finance_agent = create_react_agent(llm, 
                                   tools=[balance_sheet, income_statement, cash_flow, ratio], 
                                   state_modifier="Your task is to provide the financial data for the conversation. You can provide the balance sheet, income statement, cash flow of a company.")
finance_node = functools.partial(agent_node, agent=finance_agent, name="FinanceAgent")

supervisor = create_team_supervisor(
    llm,
    "You are a supervisor tasked with managing a conversation between the following workers: {team_members}. \
    Given the following user request, respond with the worker to act next. \
    Each worker will perform a task and respond with their results and status. \
    The workers are: CurrentDateTime, TickerSymbol, FinanceAgent. \
    The worker CurrentDateTime will provide the current date and time if user don't mention a specific time. \
    The worker TickerSymbol will provide the ticker symbol of a company if it is not provided explicitly. \
    The worker FinanceAgent will provide the financial data of a company. \
    Only use the worker FinanceAgent if already have the ticker symbol. When finished, respond with FINISH.",
    ["CurrentDateTime", "TickerSymbol", "FinanceAgent"],
)

# Create the graph here:
graph = StateGraph(StockAgentState)
graph.add_node("CurrentDateTime", current_datetime_node)
graph.add_node("TickerSymbol", check_stock_code_node)
graph.add_node("FinanceAgent", finance_node)
graph.add_node("supervisor", supervisor)

# Add the edges that always occur
graph.add_edge("CurrentDateTime", "supervisor")
graph.add_edge("TickerSymbol", "supervisor")
graph.add_edge("FinanceAgent", "supervisor")

# Add the edges where routing applies
graph.add_conditional_edges(
    "supervisor",
    lambda x: x["next"],
    {
        "CurrentDateTime": "CurrentDateTime",
        "TickerSymbol": "TickerSymbol",
        "FinanceAgent": "FinanceAgent",
        "FINISH": END,
    },
)

graph.add_edge(START, "supervisor")
chain = graph.compile()

# The following functions interoperate between the top level graph state
# and the state of the research sub-graph
def enter_chain(message: str, members: List[str]):
    results = {
        "messages": [HumanMessage(content=message)],
        "team_members": ", ".join(members),
    }
    return results

# We reuse the enter/exit functions to wrap the graph
financial_chain = (
    functools.partial(enter_chain, members=graph.nodes)
    | graph.compile()
)


# config = {"configurable": {"thread_id": "2"}}

# for s in financial_chain.stream(
#     "Tóm tắt báo cáo doanh thu của Ngân hàng Vietcombank từ năm 2019 đến nay",
#     {"recursion_limit": 10}
# ):
#     if "__end__" not in s:
#         print(s)
#         print("---")