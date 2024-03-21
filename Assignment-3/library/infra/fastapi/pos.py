from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.errors import ClosedError, DoesNotExistError, ExistsError
from core.receipt import IReceiptProduct
from core.services import Product, ProductService, Receipt, Report, Unit, UnitService
from infra.fastapi.dependables import (
    ProductRepositoryDependable,
    ReceiptRepositoryDependable,
    UnitRepositoryDependable,
)

pos_api = APIRouter()


# post units +
# get unit with id +
# get units list +
# post products assign unique unit_id +
# get product with id different from unit id +
# get products list +
# post receipts
# get receipts with id not unit_id
# patch price
# patch closed with id
# delete receipt with id
# get sales
# Units
class CreateUnitRequest(BaseModel):
    name: str


class UnitItem(BaseModel):
    id: UUID
    name: str


class UnitItemEnvelope(BaseModel):
    unit: UnitItem


class UnitListEnvelope(BaseModel):
    units: list[UnitItem]


@pos_api.post(
    "/units", status_code=201, response_model=UnitItemEnvelope, tags=["Units"]
)
def create_unit(
    request: CreateUnitRequest, units: UnitRepositoryDependable
) -> dict[str, Unit] | JSONResponse:
    unit = Unit(**request.model_dump())
    existing_unit = units.get_by_name(unit.name)
    if existing_unit:
        return ExistsError("Unit", "name", unit.name).return_json_response()
    else:
        units.create(unit)
    return {"unit": unit}


@pos_api.get(
    "/units/{unit_id}", status_code=200, response_model=UnitItem, tags=["Units"]
)
def read_unit(unit_id: UUID, units: UnitRepositoryDependable) -> Unit | JSONResponse:
    try:
        return units.read(unit_id)
    except DoesNotExistError:
        return DoesNotExistError("Unit", str(unit_id)).return_json_response()


@pos_api.get("/units", response_model=UnitListEnvelope, tags=["Units"])
def read_all(
    units: UnitRepositoryDependable, author_starts_with: str = ""
) -> dict[str, list[Unit]]:
    return {"units": UnitService(units).filter_author(author_starts_with)}


class CreateProductRequest(BaseModel):
    unit_id: UUID
    name: str
    barcode: str
    price: int


class ProductItem(BaseModel):
    id: UUID
    unit_id: UUID
    name: str
    barcode: str
    price: int


class ProductItemEnvelope(BaseModel):
    product: ProductItem


class ProductListEnvelope(BaseModel):
    products: List[ProductItem]


class UpdateProductRequest(BaseModel):
    price: int


@pos_api.post(
    "/products", status_code=201, response_model=ProductItemEnvelope, tags=["Products"]
)
def create_product(
    request: CreateProductRequest,
    products: ProductRepositoryDependable,
    units: UnitRepositoryDependable,
) -> JSONResponse | dict[str, Product]:
    product = Product(**request.model_dump())
    existing_product = products.get_by_barcode(product.barcode)
    existing_unit = units.is_created(product.unit_id)
    if not existing_unit:
        return DoesNotExistError("Unit", str(product.unit_id)).return_json_response()
    else:
        if existing_product:
            return ExistsError(
                "Product", "barcode", product.barcode
            ).return_json_response()
        else:
            products.create(product)
    return {"product": product}


@pos_api.get(
    "/products/{product_id}",
    status_code=200,
    response_model=ProductItem,
    tags=["Products"],
)
def get_single_product(
    product_id: UUID, products: ProductRepositoryDependable
) -> Product | JSONResponse:
    try:
        return products.read(product_id)
    except DoesNotExistError:
        return DoesNotExistError("Products", str(product_id)).return_json_response()


@pos_api.get("/products", response_model=ProductListEnvelope, tags=["Products"])
def read_all_products(
    products: ProductRepositoryDependable, name_start_with: str = ""
) -> dict[str, list[Product]]:
    return {"products": ProductService(products).filter_name(name_start_with)}


@pos_api.patch(
    "/products/{product_id}",
    response_model=ProductItem,
    status_code=200,
    tags=["Products"],
)
def update_product_price(
    product_id: UUID,
    request: UpdateProductRequest,
    products: ProductRepositoryDependable,
) -> Product | JSONResponse:
    try:
        product = products.read(product_id)
        if product:
            products.update_price(product_id, request.price)
        return product
    except DoesNotExistError:
        return DoesNotExistError("Product", str(product_id)).return_json_response()


class ProductForReceiptItem(BaseModel):
    id: UUID
    quantity: int
    price: float
    total: float


class ReceiptItem(BaseModel):
    id: UUID
    status: str
    products: List[ProductForReceiptItem]
    total: int


class CreateReceiptRequest(BaseModel):
    status: str = "open"
    products: List[ProductForReceiptItem] = []
    total: float


class ReceiptItemEnvelope(BaseModel):
    receipt: ReceiptItem


class ReceiptListEnvelope(BaseModel):
    receipts: List[ReceiptItem]


@pos_api.post(
    "/receipts", status_code=201, response_model=ReceiptItemEnvelope, tags=["Receipts"]
)
def create_receipt(
    request: CreateReceiptRequest, receipts: ReceiptRepositoryDependable
) -> JSONResponse | dict[str, Receipt]:
    receipt = Receipt(**request.model_dump())
    product_size = len(receipt.products)
    if product_size:
        return DoesNotExistError("Product", str(receipt.id)).return_json_response()
    else:
        receipts.create(receipt)
    return {"receipt": receipt}


@pos_api.get(
    "/receipts/{id}", status_code=200, response_model=ReceiptItem, tags=["Receipts"]
)
def get_single_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> Receipt | JSONResponse:
    try:
        # print(receipt_id)
        return receipts.read(receipt_id)
    except DoesNotExistError:
        return DoesNotExistError("Receipt", str(receipt_id)).return_json_response()


class UpdateReceiptRequest(BaseModel):
    status: str


@pos_api.patch(
    "/receipts/{receipt_id}",
    response_model=ReceiptItem,
    status_code=200,
    tags=["Receipts"],
)
def update_receipt_status(
    receipt_id: UUID,
    request: UpdateReceiptRequest,
    receipts: ReceiptRepositoryDependable,
) -> Receipt | JSONResponse:
    try:
        receipt = receipts.read(receipt_id)
        if receipt:
            if receipt.status != "closed":
                receipts.update_receipt_status(receipt_id, request.status)
            else:
                return ClosedError("Receipt", str(receipt_id)).return_json_response()
        return JSONResponse(content={}, status_code=200)
    except DoesNotExistError:
        return DoesNotExistError("Receipt", str(receipt_id)).return_json_response()


@pos_api.delete(
    "/receipts/{receipt_id}",
    response_model=ReceiptItem,
    status_code=200,
    tags=["Receipts"],
)
def delete_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> Receipt | JSONResponse:
    try:
        receipt = receipts.read(receipt_id)
        if receipt:
            if receipt.status != "closed":
                receipts.delete_receipt(receipt_id)
            else:
                return ClosedError("Receipt", str(receipt_id)).return_json_response()
        return JSONResponse(content={}, status_code=200)
    except DoesNotExistError:
        return DoesNotExistError("Receipt", str(receipt_id)).return_json_response()


class CreateProductForReceiptRequest(BaseModel):
    id: UUID
    quantity: int


@pos_api.post(
    "/receipts/{receipt_id}/products",
    status_code=201,
    response_model=ReceiptItem,
    tags=["Receipts"],
)
def add_product_to_receipt(
    receipt_id: UUID,
    product_info: CreateProductForReceiptRequest,
    products: ProductRepositoryDependable,
    receipts: ReceiptRepositoryDependable,
) -> Receipt | JSONResponse:
    receipt = receipts.get_by_id(receipt_id)
    if receipt is None:
        return DoesNotExistError("Receipt", str(receipt_id)).return_json_response()
    receipt_item = receipts.read(receipt_id)
    exists_product = products.is_created(product_info.id)
    if not exists_product:
        return DoesNotExistError("Product", str(product_info.id)).return_json_response()
    prod = products.read(product_info.id)
    product = IReceiptProduct(
        id=str(product_info.id),
        quantity=product_info.quantity,
        price=prod.price,
        total=product_info.quantity * prod.price,
    )
    receipt_item.products.append(product)
    receipt_item.total += product.total
    new_receipt = Receipt(
        receipt_item.status, receipt_item.products, receipt_item.total, receipt_id
    )
    receipts.set_item(receipt_id, new_receipt)
    return receipts.read(receipt_id)


class ReportItem(BaseModel):
    n_receipts: int
    revenue: float
    id: UUID


class ReportItemEnvelope(BaseModel):
    report: ReportItem


@pos_api.get("/sales", response_model=ReportItemEnvelope, tags=["Sales"])
def read_report(receipts: ReceiptRepositoryDependable) -> dict[str, ReportItem]:
    n_receipts = receipts.get_closed_count()
    revenue = receipts.get_revenue_count()

    report = Report(id=uuid4(), n_revenue=n_receipts, total=revenue)

    report_item = ReportItem(
        id=report.id,
        n_receipts=report.n_revenue,
        revenue=report.total,
    )

    return {"report": report_item}
