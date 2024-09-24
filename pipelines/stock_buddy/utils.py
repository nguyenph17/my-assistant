from datetime import datetime
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool(parse_docstring=True)
def get_current_datetime() -> str:
    """
    This function returns the current date and time if user mentions a relative time like "now", "today", "yesterday", "tomorrow", etc.

    Returns:
        str: The current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")






