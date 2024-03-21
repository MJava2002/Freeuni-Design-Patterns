import random
from typing import Protocol

from app.characteristics import (
    BaseCharacteristics,
    LargeClaw,
    LargeTeeth,
    Leg,
    MediumClaw,
    MediumTeeth,
    NoClaw,
    NoTeeth,
    SmallClaw,
    SmallTeeth,
    Wing,
)


class IRandomizer(Protocol):
    def stamina(self) -> int:
        pass

    def health(self) -> int:
        pass

    def power(self) -> int:
        pass

    def position(self) -> int:
        pass

    def random_characteristics(self) -> list[BaseCharacteristics]:
        pass


class DefaultRandomizer(IRandomizer):
    def stamina(self) -> int:
        return random.randint(0, 100)

    def health(self) -> int:
        return random.randint(0, 50)

    def power(self) -> int:
        return random.randint(1, 10)

    def position(self) -> int:
        return random.randint(0, 1000)

    def random_characteristics(self) -> list[BaseCharacteristics]:
        characteristics: list[BaseCharacteristics] = []
        num_legs = random.randint(0, 2)
        characteristics.append(Leg(num_legs))

        num_wings = random.randint(0, 2)
        wings = Wing(num_wings)
        characteristics.append(wings)

        claw_sizes = [NoClaw, SmallClaw, MediumClaw, LargeClaw]
        claw = random.choice(claw_sizes)()
        characteristics.append(claw)

        teeth_sizes = [NoTeeth, SmallTeeth, MediumTeeth, LargeTeeth]
        teeth = random.choice(teeth_sizes)()
        characteristics.append(teeth)
        return characteristics
