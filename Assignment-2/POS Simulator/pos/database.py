import os
import sqlite3
from os.path import abspath, dirname, join
from sqlite3 import Connection, Cursor, connect
from typing import Dict, List, Protocol, Tuple, TypeVar

from pos.constants import (
    DISCOUNT_DB_NAME,
    DISCOUNT_TABLE_NAME,
    MARKET_TABLE_NAME,
    PRODUCT_DB_NAME,
    PRODUCT_TABLE_NAME,
)
from pos.products import IProduct, Pack, SingleProduct

T = TypeVar("T")


class IDataBase(Protocol[T]):
    def get_all(self) -> List[T]:
        pass

    def add(self, info: T) -> None:
        pass


class MarketDataBase(IDataBase[Dict[str, int]]):
    def __init__(self) -> None:
        self.name: str = MARKET_TABLE_NAME
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS market_reports
                (
                    name          TEXT,
                    product_count INTEGER
                );"""
        )
        con.commit()
        con.close()

    def add(self, info: Dict[str, int]) -> None:
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        for prod in info:
            insert_query = (
                "INSERT INTO market_reports (name, product_count) VALUES (?, ?)"
            )
            values = (prod, info[prod])
            cur.execute(insert_query, values)
        con.commit()
        con.close()

    def get_all(self) -> List[Dict[str, int]]:
        con: Connection = connect(self.name)
        cur: Cursor = con.cursor()
        cur.execute("SELECT * FROM market_reports")
        products_data = cur.fetchall()
        result: List[Dict[str, int]] = []
        tmp: Dict[str, int] = {}
        for prod_data in products_data:
            tmp[prod_data[0]] = prod_data[1]
        result.append(tmp)
        cur.close()
        con.close()
        return result


class ShopDataBase(IDataBase[IProduct]):
    def __init__(self) -> None:
        self.name: str = PRODUCT_TABLE_NAME
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, PRODUCT_DB_NAME)
        with open(script_path, "r") as script_file:
            table_creation_script = script_file.read()
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.executescript(table_creation_script)
        con.commit()
        con.close()

    def add(self, info: IProduct) -> None:
        pass

    def get_all(self) -> List[IProduct]:
        con: Connection = connect(self.name)
        cur: Cursor = con.cursor()
        cur.execute("SELECT * FROM products")
        products_data = cur.fetchall()
        products: List[IProduct] = []
        for product_data in products_data:
            if product_data[3] is not None:
                products.append(
                    Pack(
                        SingleProduct(product_data[0], product_data[1]),
                        product_data[3],
                    )
                )
            else:
                products.append(
                    SingleProduct(
                        product_data[0],
                        product_data[1],
                    )
                )
        cur.close()
        con.close()
        return products


class DiscountDataBase(IDataBase[Tuple[str, int]]):
    def __init__(self) -> None:
        self.name: str = DISCOUNT_TABLE_NAME
        script_dir = dirname(abspath(__file__))
        script_path = join(script_dir, DISCOUNT_DB_NAME)

        with open(script_path, "r") as script_file:
            table_creation_script = script_file.read()
        con = connect(self.name)
        cur = con.cursor()
        cur.executescript(table_creation_script)
        con.commit()
        con.close()

    def add(self, info: Tuple[str, int]) -> None:
        pass

    def get_all(self) -> List[Tuple[str, int]]:
        con: Connection = connect(self.name)
        cur: Cursor = con.cursor()
        cur.execute("SELECT * FROM discounts")
        discount_data = cur.fetchall()
        result: List[Tuple[str, int]] = []
        for disc_data in discount_data:
            result.append((disc_data[0], disc_data[1]))
        cur.close()
        con.close()
        return result
