from pos.market import MarketInfo
from pos.pos_simulator import PosSimulator
from pos.shop import ShopInfo


class PosSystem:
    def simulate(self):
        PosSimulator.simulate()

    def generate_report(self):
        MarketInfo.print_all_market_data()

    def list_store_info(self):
        ShopInfo.print_list_info()
