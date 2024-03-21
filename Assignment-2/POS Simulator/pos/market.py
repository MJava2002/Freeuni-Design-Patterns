from typing import Dict, List

from pos.database import IDataBase, MarketDataBase
from pos.products import IProduct


class MarketInfo:
    @staticmethod
    def print_all_market_data():
        market = Market()
        all_products: List[Dict[str, int]] = market.get_all()
        info: str = ""
        info += "MARKET INFORMATION\n"
        info += "PRODUCT NAME | UNITS\n"
        for each in all_products:
            for name in each:
                info += f"{name}  | {each[name]}\n"
        print(info)


class Market:
    sold_products: Dict[IProduct, int] = {}
    revenue: float = 0
    market_db: IDataBase = MarketDataBase()

    def add_to_db(self, products: Dict[IProduct, int]) -> None:
        res: Dict[str, int] = {}
        for prod in products:
            res[prod.get_name()] = products[prod]
        self.market_db.add(res)

    def get_all(self) -> List[Dict[str, int]]:
        return self.market_db.get_all()

    def add_product(self, product: IProduct) -> None:
        if product in self.sold_products:
            self.sold_products[product] += product.get_product_count()
        else:
            self.sold_products[product] = product.get_product_count()

    def get_sold_products(self) -> Dict[IProduct, int]:
        return self.sold_products

    def print_report(self) -> None:
        print("-----Register Report-----")
        print("Product  |  Sales")
        print("----------------------")
        for item, units in self.sold_products.items():
            print(f"{item.get_name()}  |  {units}\n")
        print(f"Total Revenue: {self.revenue}\n")

    def clear_cash_register(self):
        self.add_to_db(self.sold_products)
        self.revenue = 0
        self.sold_products.clear()

    def change_revenue(self, diff: float) -> None:
        self.revenue += diff

    def get_all_revenue(self) -> float:
        return self.revenue
