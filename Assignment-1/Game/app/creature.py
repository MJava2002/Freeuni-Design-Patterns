from app.characteristics import (
    AttackPowerManager,
    CharacteristicsManager,
    MovementManager,
)
from app.logger import Logger, PredatorLogger, PreyLogger
from app.randomizer import DefaultRandomizer, IRandomizer


class Creature:
    def __init__(self, logger: Logger, name: str, randomizer: IRandomizer) -> None:
        self.logger = logger
        self.name = name

        self.health: int = randomizer.health()
        self.stamina: int = randomizer.stamina()
        self.attack_power: int = randomizer.power()

        self.position = 0
        self.characteristics = randomizer.random_characteristics()
        self.characteristics_manager = CharacteristicsManager()
        self.movement_manager = MovementManager()
        self.attack_power_manager = AttackPowerManager(self.attack_power)

    def evolve(self) -> None:
        for ch in self.characteristics:
            self.characteristics_manager.add_characteristic(ch)
        self.characteristics_manager.evolve(
            self.movement_manager, self.attack_power_manager
        )
        self.attack_power = self.attack_power_manager.get_power()

    def move(self) -> None:
        speed, loss = self.movement_manager.move(self.stamina)
        self.stamina -= loss
        self.position += speed

    def attack(self, target: "Creature") -> None:
        pass

    def print_win_message(self) -> None:
        pass


class Predator(Creature):
    def __init__(self, logger: Logger, randomizer: IRandomizer) -> None:
        super().__init__(logger, "Predator", randomizer)
        self.position: int = 0

    def evolve(self) -> None:
        super().evolve()
        self.logger.log_evolutions()
        self.logger.log_characteristics(
            self.position, self.attack_power, self.health, self.stamina
        )

    def get_position(self) -> int:
        return self.position

    def attack(self, prey: "Creature") -> None:
        while self.health > 0 and prey.health > 0:
            prey.health -= self.attack_power
            if prey.health <= 0:
                break
            self.health -= prey.health
        self.print_win_message() if prey.health <= 0 else prey.print_win_message()

    def print_win_message(self) -> None:
        self.logger.print_win_message()

    def get_stamina(self) -> int:
        return self.stamina


class Prey(Creature):
    def __init__(self, logger: Logger, randomizer: IRandomizer) -> None:
        super().__init__(logger, "Prey", randomizer)
        self.position = randomizer.position()

    def evolve(self) -> None:
        super().evolve()
        self.logger.log_evolutions()
        self.logger.log_characteristics(
            self.position, self.attack_power, self.health, self.stamina
        )

    def get_position(self) -> int:
        return self.position

    def print_win_message(self) -> None:
        self.logger.print_win_message()


class CreatureBuilder:
    logger: Logger
    randomizer: DefaultRandomizer

    def logger_method(self, logger: Logger) -> "CreatureBuilder":
        self.logger: Logger = logger
        return self

    def randomizer_method(self, randomizer: DefaultRandomizer) -> "CreatureBuilder":
        self.randomizer = randomizer
        return self

    def build_predator(self) -> "Predator":
        predator = Predator(self.logger, self.randomizer)
        return predator

    def build_prey(self) -> "Prey":
        prey = Prey(self.logger, self.randomizer)
        return prey

    def predator_logger(self) -> "CreatureBuilder":
        self.logger = PredatorLogger()
        return self

    def prey_logger(self) -> "CreatureBuilder":
        self.logger = PreyLogger()
        return self
