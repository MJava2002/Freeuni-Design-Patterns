import random
from dataclasses import dataclass
from typing import List, Protocol

from pos.payment import IPayment, RandomPaymentMethod
from pos.products import IProduct


class IProductRandomizer(Protocol):
    def randomize_product(self, products: List[IProduct]) -> List[IProduct]:
        pass


class ProductRandomizer(IProductRandomizer):
    def randomize_product(self, products: List[IProduct]) -> List[IProduct]:
        result: List[IProduct] = []
        amount: int = random.randint(0, len(products))

        for i in range(amount):
            result.append(random.choice(products))
        return result


@dataclass
class Customer:
    payment_options: List[str]
    payment_interface: IPayment
    product_random: IProductRandomizer

    def __init__(self, payment_options: List[str]) -> None:
        self.my_products: List[IProduct] = []
        self.payment_options = payment_options
        self.product_random = ProductRandomizer()
        self.payment_interface = RandomPaymentMethod()

    def select_products(self, all_products: List[IProduct]) -> None:
        self.my_products = self.product_random.randomize_product(all_products)

    def get_selected_products(self) -> List[IProduct]:
        return self.my_products

    def pay(self) -> None:
        print(
            "Customer paid with",
            self.payment_interface.payment_method(self.payment_options),
        )
