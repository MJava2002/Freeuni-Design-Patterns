from typing import List

from pos.payment import IPayment


class BarterPaymentMethod(IPayment):
    def payment_method(self, options: List[str]) -> str:
        return options[0]


def test_barter_payment_method() -> None:
    options: List[str] = ["potato", "cash", "card"]
    assert BarterPaymentMethod().payment_method(options) == "potato"
