from datetime import datetime
from duckduckgo_search import AsyncDDGS
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def get_current_datetime() -> str:
    """
    This function returns the current date and time if user mentions a relative time like "now", "today", "yesterday", "tomorrow", etc.

    Returns:
        str: The current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_stock_code(query: str) -> str:
    """
    This function searches for the stock code of a company by its name from conversation.
    Only use this function if the user request is related to stock code and the conversation don't have stock code yet.
    Args:
        query (str): The name of the company.
    
    Returns:
        str: The stock code of the company.
    """
    # search tool for stock code
    tavily_tool = TavilySearchResults(max_results=3)
    tavily_tool.invoke(query)

    query = query + " \n Lưu ý: Câu trả lời của bạn chỉ cần là mã chứng khoán."
    results = AsyncDDGS().achat(query, model="gpt-4o-mini")
    return results




