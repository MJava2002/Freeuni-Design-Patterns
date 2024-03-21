from dataclasses import dataclass
from typing import Protocol


@dataclass
class IUnit(Protocol):
    id: str
    name: str

    def get_name(self) -> str:
        pass

    def get_id(self) -> str:
        pass

    def compare(self, other: object) -> bool:
        pass


class SingleUnit(IUnit):
    id: str
    name: str

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.id

    def compare(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name and self.id == other.id
