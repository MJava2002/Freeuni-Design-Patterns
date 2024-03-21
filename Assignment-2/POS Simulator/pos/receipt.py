from typing import Iterator, List, Optional, Protocol

from pos.products import IProduct


class IReceipt(Protocol):
    def get_products(self) -> List[IProduct]:
        pass

    def __iter__(self) -> Iterator[IProduct]:
        pass


class IReceiptBuilder(Protocol):
    def product(self, product: IProduct) -> None:
        pass

    def build(self) -> IReceipt:
        pass

    def clear(self) -> None:
        pass


class Receipt(IReceipt):
    def __init__(self, products: List[IProduct]):
        self.products = products

    def get_products(self) -> List[IProduct]:
        return self.products.copy()

    def __iter__(self) -> Iterator[IProduct]:
        return iter(self.products)


class ReceiptBuilder:
    def __init__(self, kwargs: Optional[List[IProduct]] = None):
        self.args = kwargs or []

    def product(self, product: IProduct) -> None:
        self.args.append(product)

    def build(self) -> IReceipt:
        return Receipt(self.args)

    def clear(self) -> None:
        self.args = []
