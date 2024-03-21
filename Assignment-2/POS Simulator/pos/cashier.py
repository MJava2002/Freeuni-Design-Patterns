from typing import List

from pos.market import Market
from pos.products import IProduct
from pos.receipt import IReceipt, IReceiptBuilder
from pos.shop import Shop


class Cashier:
    receipt: IReceiptBuilder

    def __init__(self, market: Market, shop: Shop):
        self.market = market
        self.shop = shop
        self.discount_strategy = self.shop.get_discount_strategy()
        self.discount_options = self.shop.get_all_available_discounts()

    def open_receipt(self, receipt: IReceiptBuilder) -> None:
        self.receipt = receipt

    def add_products(self, products: List[IProduct]) -> None:
        for prod in products:
            self.receipt.product(prod)
            self.market.add_product(prod)

    def get_price_sum(self, product: IProduct) -> float:
        total_price: float = 0

        if product.get_name() in self.discount_options:
            price = self.discount_strategy.apply_discount(
                product.get_price(),
                product.get_product_count(),
                self.discount_options[product.get_name()],
            )
        else:
            price = product.get_price() * product.get_product_count()
        total_price += price
        self.market.change_revenue(total_price)
        return total_price

    def close_receipt(self) -> None:
        self.receipt.clear()

    def return_receipt(self) -> IReceipt:
        return self.receipt.build()

    def print_receipt(self) -> None:
        print("--RECEIPT--")
        print("Product    | Units | Price | Total |")
        print("-------------------------------------")
        customer_receipt = self.return_receipt()
        customer_receipt_iterator = iter(customer_receipt)
        for prod in customer_receipt_iterator:
            name = prod.get_name()
            count = prod.get_product_count()
            original_price = prod.get_price()
            total_product = self.get_price_sum(prod)
            print(f"{name} | {count} | {original_price} | {total_product}|")

    def make_z_report(self) -> bool:
        print("Do You want to make Z report?")
        inp: str = input()

        if inp == "y":
            print("clear")
            self.market.clear_cash_register()
        print("")

        return inp == "y"
