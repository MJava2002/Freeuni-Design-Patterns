from typing import List

from pos.custumer import ProductRandomizer
from pos.products import IProduct, SingleProduct


class OneProductChooser:
    def randomize_product(self, products: List[IProduct]) -> List[IProduct]:
        res: List[IProduct] = [products[len(products) - 1]]
        return res


def test_product_randomizer() -> None:
    randomizer = ProductRandomizer()
    products: List[IProduct] = [
        SingleProduct("Bon", 10.0, 1),
        SingleProduct("Choco", 12.0, 1),
    ]
    res: List[IProduct] = randomizer.randomize_product(products)
    assert 0 <= len(res) <= len(products)


def test_one_product_chooser() -> None:
    chooser = OneProductChooser()
    products: List[IProduct] = [
        SingleProduct("Bon", 10.0, 1),
        SingleProduct("Choco", 12.0, 1),
    ]
    res: List[IProduct] = chooser.randomize_product(products)
    test_res: List[IProduct] = [SingleProduct("Choco", 12.0, 1)]
    assert len(res) == 1
    assert res == test_res
