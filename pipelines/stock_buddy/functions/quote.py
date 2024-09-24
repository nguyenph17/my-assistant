from vnstock3 import Vnstock
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from typing import Optional, Literal, Annotated, List
from pandas import DataFrame
import pandas as pd

from stock_buddy.functions.helper import invoke_agent_with_dataframe

@tool(parse_docstring=True)
def history(symbol: str, 
            start: str, 
            end: Optional[str], 
            interval: Optional[str] = "1D", 
            count_back: Optional[int]=365, 
            source: Literal["VCI", "TCBS"]="VCI") -> str:
    """
    This function retrieves historical price data for a given symbol.
    Args:
        symbol: The symbol of the company.
        start: The start time for data retrieval. Can be a string in the format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS".
        end: The end time for data retrieval. Defaults to None, which means the current time will be used. Can be a string in the format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS".
        interval: The time interval for extracting historical price data. Acceptable values are: 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M. Defaults to "1D".
        count_back: The number of days to go back if the end date is not provided. Default is 365.
        source: The source of the data. Default is "VCI".

    Returns:
        DataFrame: A DataFrame containing historical price data for the given symbol.
    """
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.quote.history(start=start, end=end, interval=interval, count_back=count_back)
        if df is not None and not df.empty:
            return df
    stock = Vnstock().stock(symbol=symbol, source="TCBS")
    df = stock.quote.history(start=start, end=end, interval=interval, count_back=count_back)
    return df


def intraday(symbol: str, 
             source: Literal["VCI", "TCBS"] = "VCI", 
             page_size: Optional[int]=10_000, 
             last_time: Optional[str]=None) -> DataFrame:
    """
    This function retrieves intraday price data for a given symbol.
    
    Args:
        symbol: The symbol of the company.
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
        page_size: The number of data points to retrieve. Default is 100.
        last_time: The last time of the last data point. Default is None.

    Returns:
        DataFrame: A DataFrame containing intraday price data for the given symbol.
    """
    
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.quote.intraday(page_size=page_size, last_time=last_time)
        if df is not None and not df.empty:
            return df
        
    source = "TCBS"
    stock = Vnstock().stock(symbol=symbol, source=source)
    df = stock.quote.intraday(page_size=page_size, last_time=last_time)
    return df


def price_depth(symbol: str, 
                source: Literal["VCI", "TCBS"] = "VCI") -> DataFrame:
    """
    This function retrieves price depth data for a given symbol.
    
    Args:
        symbol: The symbol of the company.
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.

    Returns:
        DataFrame: A DataFrame containing price depth data for the given symbol.
    """
    
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.quote.price_depth()
        if df is not None and not df.empty:
            return df
        
    source = "TCBS"
    stock = Vnstock().stock(symbol=symbol, source=source)
    df = stock.quote.price_depth()
    return df


def price_board(symbols: List[str], 
                std_columns: Literal[True, False] = True, 
                source: Literal["VCI", "TCBS"] = "VCI") -> DataFrame:
    """
    This function returns the price board of a company by its symbol.
    
    Args:
        symbol: The list of symbols of the companies.
        std_columns: Whether to return the standard columns. Default is True. False will return the extended columns.
        source: The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
    
    Returns:
        DataFrame: The price board of the company.
    
    """
    if source == "VCI":
        stock = Vnstock().stock(source=source)
        df = stock.trading.price_board(symbols_list=symbols)
        if df is not None and not df.empty:
            return df
    
    stock = Vnstock().stock(source="TCBS")
    df = stock.trading.price_board(symbols_list=symbols, std_columns=std_columns)
    return df