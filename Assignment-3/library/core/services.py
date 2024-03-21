from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Protocol
from uuid import UUID, uuid4

from core.products import IProduct
from core.receipt import IReceiptProduct


@dataclass
class UnitService:
    units: UnitRepository

    def filter_author(self, name: str) -> list[Unit]:
        all_units = self.units.read_all()
        return [unit for unit in all_units if unit.name.startswith(name)]


class UnitRepository(Protocol):
    def create(self, unit: Unit) -> None:
        pass

    def read(self, unit_id: UUID) -> Unit:
        pass

    def read_all(self) -> list[Unit]:
        pass

    def get_by_name(self, name: str) -> Optional[Unit]:
        pass

    def is_created(self, unit_id: UUID) -> bool:
        pass


@dataclass
class Unit:
    name: str
    id: UUID = field(default_factory=uuid4)


# Product services
@dataclass
class Product:
    name: str
    unit_id: str
    barcode: str
    price: int
    id: UUID = field(default_factory=uuid4)


class ProductRepository(Protocol):
    def create(self, product: Product) -> None:
        pass

    def read(self, product_id: UUID) -> Product:
        pass

    def read_all_products(self) -> list[Product]:
        pass

    def update_price(self, product_id: UUID, price: int) -> IProduct:
        pass

    def is_created(self, unit_id: UUID) -> bool:
        pass

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        pass


@dataclass
class ProductService:
    products: ProductRepository

    def filter_name(self, name: str) -> list[Product]:
        all_products = self.products.read_all_products()
        return [product for product in all_products if product.name.startswith(name)]


# Receipt Service
@dataclass
class Receipt:
    status: str
    products: List[IReceiptProduct]
    total: float
    id: UUID = field(default_factory=uuid4)


class ReceiptRepository(Protocol):
    def create(self, receipt: Receipt) -> None:
        pass

    def read(self, receipt_id: UUID) -> Receipt:
        pass

    def read_all_receipts(self) -> list[Receipt]:
        pass

    def update_receipt_status(self, receipt_id: UUID, status: str) -> IReceiptProduct:
        pass

    def delete_receipt(self, receipt_id: UUID) -> None:
        pass

    def get_by_id(self, receipt_id: UUID) -> IReceiptProduct:
        pass

    def set_item(self, receipt_id: UUID, receipt: Receipt) -> None:
        pass

    def get_closed_count(self) -> int:
        pass

    def get_revenue_count(self) -> float:
        pass


@dataclass
class ReceiptService:
    receipts: ReceiptRepository

    def filter_receipt(self, name: str) -> list[Receipt]:
        all_receipts = self.receipts.read_all_receipts()
        return [receipt for receipt in all_receipts if receipt.status.startswith(name)]


# Report Services
@dataclass
class Report:
    n_revenue: int = 0
    total: float = 0
    id: UUID = field(default_factory=uuid4)


class ReportRepository(Protocol):
    def create(self, reports: Report) -> None:
        pass

    def read_report(self, report_id: UUID) -> Report:
        pass


@dataclass
class ReportService:
    report: ReportRepository
