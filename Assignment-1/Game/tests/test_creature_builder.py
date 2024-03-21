from unittest.mock import MagicMock

from app.creature import CreatureBuilder
from app.logger import Logger
from app.randomizer import DefaultRandomizer


def test_logger_method() -> None:
    builder = CreatureBuilder()
    mock_logger = MagicMock(Logger)
    result = builder.logger_method(mock_logger)
    assert result == builder
    assert builder.logger == mock_logger


def test_randomizer_method() -> None:
    builder = CreatureBuilder()
    mock_randomizer = MagicMock(DefaultRandomizer)
    result = builder.randomizer_method(mock_randomizer)
    assert result == builder
    assert builder.randomizer == mock_randomizer


def test_build_predator() -> None:
    builder = CreatureBuilder()
    mock_logger = MagicMock(Logger)
    mock_randomizer = MagicMock(DefaultRandomizer)
    builder.logger = mock_logger
    builder.randomizer = mock_randomizer
    predator = builder.build_predator()
    assert predator.logger == mock_logger


def test_build_prey() -> None:
    builder = CreatureBuilder()
    mock_logger = MagicMock(Logger)
    mock_randomizer = MagicMock(DefaultRandomizer)
    builder.logger = mock_logger
    builder.randomizer = mock_randomizer
    prey = builder.build_prey()
    assert prey.logger == mock_logger
