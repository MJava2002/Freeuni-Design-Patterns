from sqlite3 import Connection, Cursor, connect
from typing import Optional

from core.units import IUnit, SingleUnit


class SqliteUnitRepository:
    def __init__(self, db_name: str) -> None:
        self.db_name = f"database/{db_name}"

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS units
                (unit_id TEXT, unit_name TEXT)
            """
        )

        con.commit()
        con.close()

    def clear(self) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("DELETE FROM units")

        con.commit()
        cur.close()

    def create(self, unit: IUnit) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT unit_id FROM products WHERE unit_id=?", unit.id)
        query: list[str] = cur.fetchall()

        if len(query) == 0:
            cur.execute(
                "INSERT INTO units VALUES (?, ?)",
                (unit.id, unit.name),
            )

        con.commit()
        con.close()

    def fetch_all(self) -> dict[str, IUnit]:
        all_units = dict[str, IUnit]()

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT * FROM units")
        unit_list: list[tuple[str, str]] = cur.fetchall()

        all_units.update(
            map(
                lambda item: (item[0], self.get_item(item[0], item[1])),
                unit_list,
            )
        )

        con.commit()
        con.close()

        return all_units

    def fetch_one(self, key: str) -> Optional[IUnit]:
        unit: Optional[IUnit] = None

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT unit_id, unit_name FROM units WHERE unit_id=?", (key,))
        unit_info: Optional[tuple[str, str]] = cur.fetchone()

        if unit_info is not None:
            unit = self.get_item(unit_info[0], unit_info[1])

        con.commit()
        con.close()

        return unit

    def get_item(self, unit_id: str, name: str) -> IUnit:
        return SingleUnit(unit_id, name)
