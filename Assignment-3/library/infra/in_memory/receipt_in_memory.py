from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from core.errors import DoesNotExistError
from core.services import Receipt


@dataclass
class ReceiptInMemory:
    receipts: dict[UUID, Receipt] = field(default_factory=dict)

    def create(self, receipt: Receipt) -> None:
        self.receipts[receipt.id] = receipt

    def read(self, receipt_id: UUID) -> Receipt:
        try:
            return self.receipts[receipt_id]
        except KeyError:
            raise DoesNotExistError("Receipt", str(receipt_id))

    def read_all_receipts(self) -> list[Receipt]:
        return list(self.receipts.values())

    def get_closed_count(self) -> int:
        count: int = 0
        for receipt in self.receipts.values():
            if receipt.status == "closed":
                count += 1
        print(count)
        return count

    def get_revenue_count(self) -> float:
        revenue: float = 0
        for receipt in self.receipts.values():
            if receipt.status == "closed":
                revenue += receipt.total
        print(revenue)
        return revenue

    def update_receipt_status(self, receipt_id: UUID, status: str) -> Optional[Receipt]:
        receipt = None
        for receipt in self.receipts.values():
            if receipt.id == receipt_id:
                receipt.status = status
        return receipt

    def delete_receipt(self, receipt_id: UUID) -> None:
        receipt_curr = None
        for receipt in self.receipts.values():
            if receipt.id == receipt_id:
                receipt_curr = receipt
        if receipt_curr is not None:
            self.receipts.pop(receipt_id)

    def get_by_id(self, receipt_id: UUID) -> Optional[Receipt]:
        receipt_curr = None
        for receipt in self.receipts.values():
            if receipt.id == receipt_id:
                receipt_curr = receipt
        return receipt_curr

    def set_item(self, receipt_id: UUID, receipt: Receipt) -> None:
        self.receipts[receipt_id] = receipt
