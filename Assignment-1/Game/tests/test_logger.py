import pytest

from app.logger import PredatorLogger, PreyLogger


def test_prey_logger(capsys: pytest.CaptureFixture[str]) -> None:
    prey_logger = PreyLogger()
    prey_logger.log_evolutions()
    prey_logger.print_win_message()

    assert capsys.readouterr().out == "Prey evolved\nPrey ran into infinity\n"


def test_predator_logger(capsys: pytest.CaptureFixture[str]) -> None:
    predator_logger = PredatorLogger()
    predator_logger.log_evolutions()
    predator_logger.print_win_message()
    assert (
        capsys.readouterr().out
        == "Predator evolved\nSome R-rated things have happened\n"
    )
