import os
from typing import Any
from woocommerce import API


async def get_woocomerce_products() -> list[dict[str, Any]]:
    wcapi = API(
        url=os.getenv("WOOCOMMERCE_URL"),
        consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
        consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
        version="wc/v3",
        timeout=10
    )
    response = wcapi.get("products", params={"per_page": 100, "page": 1})
    products = response.json()
    return products
