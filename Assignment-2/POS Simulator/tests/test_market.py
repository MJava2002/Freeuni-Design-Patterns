from typing import Dict

from pos.market import Market
from pos.products import IProduct, SingleProduct


def test_market() -> None:
    market = Market()
    product: IProduct = SingleProduct("Apple", 1, 1)
    products: Dict[IProduct, int] = {product: 1}
    market.add_product(product)
    assert market.get_sold_products() == products


def test_many_market() -> None:
    market = Market()
    product_one: IProduct = SingleProduct("Apple", 1, 1)
    product_two: IProduct = SingleProduct("Banana", 2, 1)
    products: Dict[IProduct, int] = {product_one: 1, product_two: 1}
    market.add_product(product_one)
    market.add_product(product_two)
    assert market.get_sold_products() == products


def test_double_product_market() -> None:
    market = Market()
    product_one: IProduct = SingleProduct("Apple", 1, 1)
    product_two: IProduct = SingleProduct("Apple", 1, 1)
    products: Dict[IProduct, int] = {product_one: 2}
    market.add_product(product_one)
    market.add_product(product_two)
    assert market.get_sold_products() == products
