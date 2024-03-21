from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from core.services import (
    ProductRepository,
    ReceiptRepository,
    ReportRepository,
    UnitRepository,
)


def get_unit_repository(request: Request) -> UnitRepository:
    return request.app.state.units  # type: ignore


def get_product_repository(request: Request) -> ProductRepository:
    return request.app.state.products  # type: ignore


def get_receipt_repository(request: Request) -> ReceiptRepository:
    return request.app.state.receipts  # type: ignore


def get_report_repository(request: Request) -> ReportRepository:
    return request.app.state.report  # type: ignore


UnitRepositoryDependable = Annotated[UnitRepository, Depends(get_unit_repository)]

ProductRepositoryDependable = Annotated[
    ProductRepository, Depends(get_product_repository)
]

ReceiptRepositoryDependable = Annotated[
    ReceiptRepository, Depends(get_receipt_repository)
]

ReportRepositoryDependable = Annotated[ReportRepository, Depends(get_report_repository)]
