from vnstock3 import Vnstock
from pandas import DataFrame
from typing import Literal, Optional

def balance_sheet(symbol: str, 
                  period: Optional[Literal["year", "quarter"]] = "year", 
                  lang: Optional[Literal["en", "vi"]] = "vi", 
                  source: Optional[Literal["VCI", "TCBS"]] = "VCI",
                  drop_na: Optional[Literal[True, False]] = True) -> DataFrame:
    """
    This function returns the balance sheet of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        period (str): The period of the balance sheet. It can be "year" or "quarter". Default is "year".
        lang (str): The language of the data. It can be "en" or "vi". Default is "vi".
        source(str): The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
        dropna (bool): Whether to drop columns with all 0 values. Default is True.
    
    Returns:
        DataFrame: The balance sheet of the company.
    
    """
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.finance.balance_sheet(period=period, lang=lang, drop_na=drop_na)
        if df is not None and not df.empty:
            return df
    
    stock = Vnstock().stock(symbol=symbol, source="TCBS")
    df = stock.finance.balance_sheet(period=period, lang=lang)
    return df


def income_statement(symbol: str, 
                  period: Optional[Literal["year", "quarter"]] = "year", 
                  lang: Optional[Literal["en", "vi"]] = "vi", 
                  source: Optional[Literal["VCI", "TCBS"]] = "VCI",
                  drop_na: Optional[Literal[True, False]] = True) -> DataFrame:
    """
    This function returns the income statement of a company by its symbol.

    Args:
        symbol (str): The symbol of the company.
        period (str): The period of the income statement. It can be "year" or "quarter". Default is "year".
        lang (str): The language of the data. It can be "en" or "vi". Default is "vi".
        source(str): The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
        dropna (bool): Whether to drop columns with all 0 values. Default is True.
    Returns:
        DataFrame: The income statement of the company.
    """
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.finance.income_statement(period=period, lang=lang, drop_na=drop_na)
        if df is not None and not df.empty:
            return df
    
    stock = Vnstock().stock(symbol=symbol, source="TCBS")
    df = stock.finance.income_statement(period=period, lang=lang)
    return df



def cash_flow(symbol: str, 
                  period: Optional[Literal["year", "quarter"]] = "year", 
                  lang: Optional[Literal["en", "vi"]] = "vi", 
                  source: Optional[Literal["VCI", "TCBS"]] = "VCI",
                  drop_na: Optional[Literal[True, False]] = True) -> DataFrame:
    """
    This function returns the cash flow of a company by its symbol.

    Args:
        symbol (str): The symbol of the company.
        period (str): The period of the cash flow. It can be "year" or "quarter". Default is "year".
        lang (str): The language of the data. It can be "en" or "vi". Default is "vi".
        source(str): The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
        dropna (bool): Whether to drop columns with all 0 values. Default is True.
    Returns:
        DataFrame: The cash flow of the company.
    """
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.finance.cash_flow(period=period, lang=lang, drop_na=drop_na)
        if df is not None and not df.empty:
            return df
    
    stock = Vnstock().stock(symbol=symbol, source="TCBS")
    df = stock.finance.cash_flow(period=period, lang=lang)
    return df

def ratio(symbol: str, 
                  period: Optional[Literal["year", "quarter"]] = "year", 
                  lang: Optional[Literal["en", "vi"]] = "vi", 
                  source: Optional[Literal["VCI", "TCBS"]] = "VCI",
                  drop_na: Optional[Literal[True, False]] = True,
                  get_all: Optional[Literal[True, False]] = True) -> DataFrame:
    """
    This function returns the ratio of a company by its symbol.

    Args:
        symbol (str): The symbol of the company.
        period (str): The period of the ratio. It can be "year" or "quarter". Default is "quarter".
        lang (str): The language of the data. It can be "en" or "vi". Default is "vi".
        source(str): The source of the data. Default is "VCI". Currently, only "VCI" and "TCBS" are supported.
        dropna (bool): Whether to drop columns with all 0 values. Default is True.
        get_all (bool): Get all the data. Default is True.
    Returns:
        DataFrame: The ratio of the company.
    """
    if source == "VCI":
        stock = Vnstock().stock(symbol=symbol, source=source)
        df = stock.finance.ratio(period=period, lang=lang, drop_na=drop_na)
        if df is not None and not df.empty:
            return df
    
    stock = Vnstock().stock(symbol=symbol, source="TCBS")
    df = stock.finance.ratio(period=period, get_all=get_all)
    return df