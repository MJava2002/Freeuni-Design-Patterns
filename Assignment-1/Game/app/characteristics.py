import random
from typing import Dict, Tuple


class MovementManager:
    def __init__(self) -> None:
        self.movements: Dict[str, Tuple[int, int, int]] = {}

    def add_movement_strategy(
        self, name: str, stamina_cost: int, speed: int, stamina_loss: int
    ) -> None:
        self.movements[name] = (stamina_cost, speed, stamina_loss)

    def move(self, creature_stamina: int) -> Tuple[int, int]:
        if not self.movements:
            return 0, 0

        valid_movements = [
            name
            for name, (stamina_cost, speed, stamina_loss) in self.movements.items()
            if creature_stamina >= stamina_cost
        ]
        if valid_movements:
            movement_name = random.choice(valid_movements)
            stamina_cost, speed, stamina_loss = self.movements[movement_name]
            return speed, stamina_loss
        return 0, 0


class AttackPowerManager:
    def __init__(self, initial_attack_power: int = 0) -> None:
        self.attack_power: int = initial_attack_power

    def get_power(self) -> int:
        return self.attack_power

    def modify_attack_power(self, value: int) -> None:
        self.attack_power += value

    def multipy_attack_power(self, value: int) -> None:
        self.attack_power *= value


class BaseCharacteristics:
    def __init__(self, num_characteristics: int = 0) -> None:
        self.num_characteristics: int = num_characteristics

    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        pass


class Leg(BaseCharacteristics):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        if self.num_characteristics >= 0:
            movement_manager.add_movement_strategy("Crawl", 0, 1, 1)
        if self.num_characteristics >= 1:
            movement_manager.add_movement_strategy("Hop", 20, 3, 2)
        if self.num_characteristics >= 2:
            movement_manager.add_movement_strategy("Walk", 40, 4, 2)
            movement_manager.add_movement_strategy("Run", 60, 6, 4)


class Wing(BaseCharacteristics):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        if self.num_characteristics >= 0:
            movement_manager.add_movement_strategy("Crawl", 0, 1, 1)
        if self.num_characteristics >= 2:
            movement_manager.add_movement_strategy("Fly", 80, 8, 4)


class Claw(BaseCharacteristics):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        pass


class NoClaw(Claw):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        pass


class SmallClaw(Claw):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.multipy_attack_power(2)


class MediumClaw(Claw):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.multipy_attack_power(3)


class LargeClaw(Claw):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.multipy_attack_power(4)


class Teeth(BaseCharacteristics):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        pass


class NoTeeth(Teeth):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        pass


class SmallTeeth(Teeth):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.modify_attack_power(3)


class MediumTeeth(Teeth):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.modify_attack_power(6)


class LargeTeeth(Teeth):
    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        attack_manager.modify_attack_power(9)


class CharacteristicsManager:
    def __init__(self) -> None:
        self.characteristics: list[BaseCharacteristics] = []

    def add_characteristic(self, characteristic: BaseCharacteristics) -> None:
        self.characteristics.append(characteristic)

    def evolve(
        self, movement_manager: MovementManager, attack_manager: AttackPowerManager
    ) -> None:
        for characteristic in self.characteristics:
            characteristic.evolve(movement_manager, attack_manager)
