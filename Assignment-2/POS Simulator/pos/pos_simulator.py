from itertools import count

from pos.cashier import Cashier
from pos.constants import CARD, CASH, SHIFTS
from pos.custumer import Customer
from pos.manager import Manager
from pos.market import Market
from pos.receipt import ReceiptBuilder
from pos.shop import Shop


class PosSimulator:
    @staticmethod
    def simulate():
        shop = Shop()
        all_products = shop.get_all_available_products()

        for i in range(SHIFTS):
            print("SHIFT ------------------------- ", i)
            market = Market()
            manager: Manager = Manager(market)
            for j in count(1):
                print("COSTUMER NUMBER----------------", j)
                payment_options = [CASH, CARD]
                customer = Customer(payment_options)
                cashier = Cashier(market, shop)
                customer.select_products(all_products)
                cashier.open_receipt(ReceiptBuilder())
                cashier.add_products(customer.get_selected_products())
                cashier.print_receipt()
                customer.pay()
                cashier.close_receipt()

                if j % 20 == 0:
                    manager.make_x_report()

                if j % 100 == 0:
                    if cashier.make_z_report():
                        break
