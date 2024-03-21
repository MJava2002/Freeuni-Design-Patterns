from app.randomizer import DefaultRandomizer


def test_stamina() -> None:
    randomizer = DefaultRandomizer()
    stamina = randomizer.stamina()
    assert 0 <= stamina <= 100


def test_health() -> None:
    randomizer = DefaultRandomizer()
    health = randomizer.health()
    assert 0 <= health <= 50


def test_power() -> None:
    randomizer = DefaultRandomizer()
    power = randomizer.power()
    assert 1 <= power <= 10


def test_position() -> None:
    randomizer = DefaultRandomizer()
    position = randomizer.position()
    assert 1 <= position <= 1000


def test_random_characteristics() -> None:
    randomizer = DefaultRandomizer()
    characteristics = randomizer.random_characteristics()
    assert len(characteristics) == 4
