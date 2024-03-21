from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from core.errors import DoesNotExistError
from core.services import Unit


@dataclass
class UnitInMemory:
    units: dict[UUID, Unit] = field(default_factory=dict)

    def create(self, unit: Unit) -> None:
        self.units[unit.id] = unit

    def read(self, unit_id: UUID) -> Unit:
        # print(unit_id)
        # return self.units[unit_id]
        try:
            return self.units[unit_id]
        except KeyError:
            raise DoesNotExistError("Units", str(unit_id))

    def read_all(self) -> list[Unit]:
        return list(self.units.values())

    def is_created(self, unit_id: UUID) -> bool:
        return unit_id in self.units

    def get_by_name(self, name: str) -> Optional[Unit]:
        for unit in self.units.values():
            if unit.name == name:
                return unit
        return None
