from dataclasses import dataclass, field


@dataclass
class IReceiptProduct:
    id: str
    quantity: int
    price: float
    total: float

    def get_id(self) -> str:
        return self.id

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> float:
        return self.price

    def get_total(self) -> float:
        return self.total

    def compare(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id


@dataclass
class IReceipt:
    id: str
    status: str
    products: list[IReceiptProduct] = field(default_factory=list[IReceiptProduct])
    total: float = 0

    def get_id(self) -> str:
        return self.id

    def get_price(self) -> float:
        return self.total

    def get_status(self) -> str:
        return self.status
