from fastapi import FastAPI

from infra.fastapi import pos_api
from infra.in_memory import ProductInMemory, ReceiptInMemory, UnitInMemory
from infra.in_memory.report_in_memory import ReportInMemory

DB_NAME = "unit.db"


def init_app() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(pos_api)
    app.state.units = UnitInMemory()
    app.state.products = ProductInMemory()
    app.state.receipts = ReceiptInMemory()
    app.state.report = ReportInMemory()
    return app
