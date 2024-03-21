from abc import ABC, abstractmethod
from dataclasses import dataclass


class IProduct(ABC):
    name: str
    price: float
    count: int

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_product_count(self) -> int:
        pass

    @abstractmethod
    def compare(self, other: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


@dataclass
class SingleProduct(IProduct):
    name: str
    price: float
    count: int = 1

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_product_count(self) -> int:
        return 1

    def compare(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.name == other.name
            and self.count == other.count
            and self.price == other.price
        )

    def __hash__(self) -> int:
        return hash((self.name, self.price))


@dataclass
class Pack(IProduct):
    product: IProduct
    pack_size: int

    def get_name(self) -> str:
        return self.product.name

    def get_price(self) -> float:
        return self.product.price

    def get_product_count(self) -> int:
        return self.pack_size

    def compare(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.name == other.name
            and self.count == other.count
            and self.price == other.price
        )

    def __hash__(self) -> int:
        return hash((self.product, self.pack_size))
