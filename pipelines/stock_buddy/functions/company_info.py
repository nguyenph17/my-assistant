from vnstock3 import Vnstock
from pandas import DataFrame

def overview(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the overview of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The overview of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.overview()


def profile(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the profile of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The profile of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.profile()


def shareholders(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the shareholders of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The shareholders of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.shareholders()


def insider_deals(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the insider deals of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The insider deals of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.insider_deals()

def subsidiaries(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the subsidiaries of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The subsidiaries of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.subsidiaries()


def officers(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the officers of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The officers of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.officers()

def events(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the events of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The events of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.events()


def news(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the news of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The news of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.news()

def dividends(symbol: str, source: str = "TCBS") -> DataFrame:
    """
    This function returns the dividends of a company by its symbol.
    
    Args:
        symbol (str): The symbol of the company.
        source(str): The source of the data. Default is "TCBS". Currently, only "TCBS" is supported.
    
    Returns:
        DataFrame: The dividends of the company.
    
    """
    company = Vnstock().stock(symbol=symbol, source=source).company
    return company.dividends()