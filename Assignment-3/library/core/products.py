from abc import ABC, abstractmethod
from dataclasses import dataclass


class IProduct(ABC):
    id: str
    unit_id: str
    name: str
    barcode: str
    price: float

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_barcode(self) -> str:
        pass

    @abstractmethod
    def get_unit_id(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def compare(self, other: object) -> bool:
        pass


@dataclass
class SingleProduct(IProduct):
    id: str
    unit_id: str
    name: str
    barcode: str
    price: float

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_barcode(self) -> str:
        return self.barcode

    def get_unit_id(self) -> str:
        return self.unit_id

    def compare(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name and self.id == other.id
