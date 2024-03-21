import random
from typing import List, Protocol


class IPayment(Protocol):
    def payment_method(self, options: List[str]) -> str:
        pass


class RandomPaymentMethod(IPayment):
    def payment_method(self, options: List[str]) -> str:
        return random.choice(options)
