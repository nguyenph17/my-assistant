from vnstock3 import Vnstock
from pandas import DataFrame
from typing import Literal, List

def price_board(symbols: List[str], 
                std_columns: Literal[True, False] = True, 
                source: Literal["VCI", "TCBS"] = "VCI") -> DataFrame:
    """
    This function returns the price board of a company by its symbol.
    
    Args:
        symbol (List[str]): The list of symbols of the companies.
        std_columns (bool): Whether to return the standard columns. Default is True. False will return the extended columns.
        source(str): The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
    
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