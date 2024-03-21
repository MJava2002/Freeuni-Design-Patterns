from typing import Protocol

from randomizer import DefaultRandomizer

from app.creature import Creature, CreatureBuilder
from app.logger import PredatorLogger, PreyLogger


class GameSimulator(Protocol):
    def play(self) -> None:
        pass


class SporeSimulation(GameSimulator):
    def __init__(self) -> None:
        randomizer = DefaultRandomizer()
        builder: CreatureBuilder = CreatureBuilder()
        self.predator = (
            builder.logger_method(PredatorLogger())
            .randomizer_method(randomizer)
            .build_predator()
        )
        self.prey = (
            builder.logger_method(PreyLogger())
            .randomizer_method(randomizer)
            .build_prey()
        )

        # self.predator = Predator(PredatorLogger(), randomizer)
        # self.prey = Prey(PreyLogger(), randomizer)

    def play(self) -> None:
        self.prey.evolve()
        self.predator.evolve()
        while True:
            if self.predator.get_position() >= self.prey.get_position():
                self.predator.attack(self.prey)
                break
            if self.predator.get_stamina() <= 0:
                self.prey.print_win_message()
                break
            self.prey.move()
            self.predator.move()

    def fight(self, creature_1: Creature, creature_2: Creature) -> None:
        while creature_1.health > 0 and creature_2.health > 0:
            creature_2.health -= creature_1.attack_power
            if creature_2.health <= 0:
                break
            creature_1.health -= creature_2.health


def run_simulation(simulation_count: int) -> None:
    for i in range(simulation_count):
        print(f"Simulation {i + 1}:")
        simulation = SporeSimulation()
        simulation.play()
        print("\n")


SIMULATION_COUNT: int = 100
if __name__ == "__main__":
    run_simulation(SIMULATION_COUNT)
