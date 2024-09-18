from datetime import datetime
from duckduckgo_search import AsyncDDGS


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_stock_code(query: str) -> str:
    query = query + " \n Lưu ý: Câu trả lời của bạn chỉ cần là mã chứng khoán."
    results = AsyncDDGS().achat(query, model="gpt-4o-mini")
    return results




