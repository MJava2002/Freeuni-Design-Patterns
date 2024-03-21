from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from core.errors import DoesNotExistError
from core.services import Product


@dataclass
class ProductInMemory:
    products: dict[UUID, Product] = field(default_factory=dict)

    def create(self, product: Product) -> None:
        self.products[product.id] = product

    def read(self, product_id: UUID) -> Product:
        try:
            return self.products[product_id]
        except KeyError:
            raise DoesNotExistError("Products", str(product_id))

    def read_all_products(self) -> list[Product]:
        return list(self.products.values())

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        for product in self.products.values():
            if product.barcode == barcode:
                return product
        return None

    def update_price(self, product_id: UUID, price: int) -> Optional[Product]:
        product = None
        for product in self.products.values():
            if product.id == product_id:
                product.price = price
        return product

    def is_created(self, product_id: UUID) -> bool:
        return product_id in self.products
