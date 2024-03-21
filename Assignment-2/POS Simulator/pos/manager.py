from pos.market import Market


class Manager:
    def __init__(self, market: Market):
        self.market = market

    def make_x_report(self) -> None:
        print("Do You want to make X report? ")
        inp: str = input()
        if inp == "y":
            self.market.print_report()
        print("")
