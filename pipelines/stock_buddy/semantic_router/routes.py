from semantic_router import Route

route_quotes = Route(
    name="quote",
    utterances=[
        "Kiểm tra giá chứng khoán mã ACB",
        "Giá cổ phiếu ACB ngày hôm nay"
    ],
    description="Giá chứng khoán"
)

trading_quotes = Route(
    name="trading",
    utterances=[
        "Kiểm tra khối lượng giao dịch mã ACB",
        "Khối lượng giao dịch cổ phiếu ACB ngày hôm nay"
    ],
    description="Giao dịch"
)


list_routes = [
    route_quotes,
    trading_quotes
]