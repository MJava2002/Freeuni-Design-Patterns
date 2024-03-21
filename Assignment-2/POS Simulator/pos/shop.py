from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from pos.database import DiscountDataBase, IDataBase, ShopDataBase
from pos.products import IProduct


class IDiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(
        self, price: float, unit: int, discount_percentage: int
    ) -> float:
        pass


class DefaultDiscount(IDiscountStrategy):
    def apply_discount(
        self, price: float, unit: int, discount_percentage: int
    ) -> float:
        return price


class PercentageDiscount(IDiscountStrategy):
    def apply_discount(
        self, price: float, unit: int, discount_percentage: int
    ) -> float:
        return unit * (price - (price * discount_percentage / 100))


class Shop:
    def __init__(
        self,
        product_repository: IDataBase = ShopDataBase(),
        discount_repository: IDataBase = DiscountDataBase(),
        discount_strategy: IDiscountStrategy = PercentageDiscount(),
    ):
        self.product_repository = product_repository
        self.discount_strategy = discount_strategy
        self.discount_repository = discount_repository

    def get_all_available_products(self) -> List[IProduct]:
        return self.product_repository.get_all()

    def get_discount_strategy(self) -> IDiscountStrategy:
        return self.discount_strategy

    def get_all_available_discounts(self) -> Dict[str, int]:
        return self.build_discount_dictionary(self.discount_repository.get_all())

    @staticmethod
    def build_discount_dictionary(disc_list: List[Tuple[str, int]]) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for prod in disc_list:
            result[prod[0]] = prod[1]
        return result


class ShopInfo:
    @staticmethod
    def print_list_info():
        shop = Shop()
        all_products: List[IProduct] = shop.get_all_available_products()
        discounts: Dict[str, int] = shop.get_all_available_discounts()
        info: str = ""
        info += "SHOP INFORMATION\n"
        info += "PRODUCT NAME | PRODUCT PRICE | UNITS | DISCOUNT\n"

        default: int = 0
        for prod in all_products:
            if prod.get_name() in discounts:
                default = discounts[prod.get_name()]
            info += (
                f"{prod.get_name()} | {prod.get_price()} |"
                f" {prod.get_product_count()} | {default}\n"
            )
            default = 0
        print(info)
