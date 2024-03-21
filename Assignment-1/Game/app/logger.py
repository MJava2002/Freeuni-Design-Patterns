from abc import ABC, abstractmethod


class Logger(ABC):
    def log_characteristics(
        self, location: int, power: int, health: int, stamina: int
    ) -> None:
        print(
            f"\tlocation: {location}\n"
            + f"\tpower: {power}\n"
            + f"\thealth: {health}\n"
            + f"\tstamina: {stamina}\n"
        )

    @abstractmethod
    def log_evolutions(self) -> None:
        pass

    @abstractmethod
    def print_win_message(self) -> None:
        pass


class ConsoleLogger(Logger, ABC):
    def log_characteristics(
        self, position: int, power: int, health: int, stamina: int
    ) -> None:
        print(
            f"\tposition: {position}\n"
            + f"\tpower: {power}\n"
            + f"\thealth: {health}\n"
            + f"\tstamina: {stamina}\n"
        )


class NullLogger(Logger):
    def log_evolutions(self) -> None:
        pass

    def print_win_message(self) -> None:
        pass


class PreyLogger(Logger):
    def log_evolutions(self) -> None:
        print("Prey evolved")

    def print_win_message(self) -> None:
        print("Prey ran into infinity")


class PredatorLogger(Logger):
    def log_evolutions(self) -> None:
        print("Predator evolved")

    def print_win_message(self) -> None:
        print("Some R-rated things have happened")


class LoggerFactory:
    @staticmethod
    def create_logger(logger_type: str) -> Logger:
        if logger_type == "Prey":
            return PreyLogger()
        return PredatorLogger()
