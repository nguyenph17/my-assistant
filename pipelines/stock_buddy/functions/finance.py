from vnstock3 import Vnstock
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from typing import Optional, Literal, Annotated

from stock_buddy.functions.helper import invoke_agent_with_dataframe

# Function to handle stock data retrieval and agent invocation
def handle_financial_data(symbol, period, lang, source, function_name, **kwargs):
    try:
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = getattr(stock.finance, function_name)(period=period, lang=lang, **kwargs)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        print(f"Error with source {source}: {e}")
        return None


@tool(parse_docstring=True, response_format="content_and_artifact")
def balance_sheet(state: Annotated[dict, InjectedState], 
                  symbol: str, 
                  period: Optional[Literal["year", "quarter"]] = "year", 
                  lang: Optional[Literal["en", "vi"]] = "vi", 
                  source: Optional[Literal["VCI", "TCBS"]] = "VCI") -> str:
    """
    This function returns the balance sheet of a company by its symbol.
    Truy xuất dữ liệu bảng cân đối kế toán của một công ty.
    
    Args:
        symbol: The symbol of the company.
        period: The period of the balance sheet. It can be "year" or "quarter". Default is "year".
        lang: The language of the data. It can be "en" or "vi". Default is "vi".
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
    
    Returns:
        str: The balance sheet of the company.
    
    """
    try:
        df = handle_financial_data(symbol, period, lang, source, "balance_sheet")
        if df is None:
            df = handle_financial_data(symbol, period, lang, "TCBS", "balance_sheet")
        return invoke_agent_with_dataframe(state, df), df
    except Exception as e:
        return f"Error: {e}", None

@tool(parse_docstring=True, response_format="content_and_artifact")
def income_statement(state: Annotated[dict, InjectedState], 
                     symbol: str, 
                     period: Optional[Literal["year", "quarter"]] = "year", 
                     lang: Optional[Literal["en", "vi"]] = "vi", 
                     source: Optional[Literal["VCI", "TCBS"]] = "VCI") -> str:
    """
    This function returns the income statement of a company by its symbol.
    Trích xuất báo cáo lợi nhuận/lãi lỗ của một công ty dựa trên mã cổ phiếu.

    Args:
        symbol: The symbol of the company, if there is no symbol, dont call this function.
        period: The period of the income statement. It can be "year" or "quarter". Default is "year".
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
    
    Returns:
        str: The income statement of the company.
    """
    try:
        df = handle_financial_data(symbol, period, lang, source, "income_statement")
        if df is None:
            df = handle_financial_data(symbol, period, lang, "TCBS", "income_statement")
        return invoke_agent_with_dataframe(state, df), df
    except Exception as e:
        return f"Error: {e}", None

@tool(parse_docstring=True, response_format="content_and_artifact")
def cash_flow(state: Annotated[dict, InjectedState], 
              symbol: str, 
              period: Optional[Literal["year", "quarter"]] = "year", 
              lang: Optional[Literal["en", "vi"]] = "vi", 
              source: Optional[Literal["VCI", "TCBS"]] = "VCI") -> str:
    """
    This function returns the cash flow (báo cáo lưu chuyển tiền tệ) of a company by its symbol.

    Args:
        symbol: The symbol of the company.
        period: The period of the cash flow. It can be "year" or "quarter". Default is "year".
        lang: The language of the data. It can be "en" or "vi". Default is "vi".
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.

    Returns:
        str: The cash flow of the company.
    """
    try:
        df = handle_financial_data(symbol, period, lang, source, "cash_flow")
        if df is None:
            df = handle_financial_data(symbol, period, lang, "TCBS", "cash_flow")
        return invoke_agent_with_dataframe(state, df), df
    except Exception as e:
        return f"Error: {e}", None

@tool(parse_docstring=True, response_format="content_and_artifact")
def ratio(state: Annotated[dict, InjectedState], 
          symbol: str, 
          period: Optional[Literal["year", "quarter"]] = "year", 
          lang: Optional[Literal["en", "vi"]] = "vi", 
          source: Optional[Literal["VCI", "TCBS"]] = "VCI") -> str:
    """
    This function returns the ratio (báo cáo chỉ số tài chính) of a company by its symbol.

    Args:
        symbol: The symbol of the company.
        period: The period of the ratio. It can be "year" or "quarter". Default is "quarter".
        lang: The language of the data. It can be "en" or "vi". Default is "vi".
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.

    Returns:
        str: The ratio of the company.
    """
    try:
        df = handle_financial_data(symbol, period, lang, source, "ratio")
        if df is None:
            df = handle_financial_data(symbol, period, lang, "TCBS", "ratio")
        return invoke_agent_with_dataframe(state, df), df
    except Exception as e:
        return f"Error: {e}", None

