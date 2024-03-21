from app.characteristics import (
    AttackPowerManager,
    CharacteristicsManager,
    Claw,
    MovementManager,
)


def test_add_movement_strategy() -> None:
    manager = MovementManager()
    manager.add_movement_strategy("TestMove", 10, 5, 2)
    assert manager.movements["TestMove"] == (10, 5, 2)


def test_move_with_valid_movement() -> None:
    manager = MovementManager()
    manager.add_movement_strategy("Walk", 20, 10, 5)
    speed, stamina_loss = manager.move(30)
    assert speed == 10
    assert stamina_loss == 5


def test_move_with_no_valid_movement() -> None:
    manager = MovementManager()
    speed, stamina_loss = manager.move(30)
    assert speed == 0
    assert stamina_loss == 0


def test_modify_attack_power() -> None:
    manager = AttackPowerManager(10)
    manager.modify_attack_power(5)
    assert manager.get_power() == 15


def test_multiply_attack_power() -> None:
    manager = AttackPowerManager(10)
    manager.multipy_attack_power(2)
    assert manager.get_power() == 20


def test_add_characteristic() -> None:
    manager = CharacteristicsManager()
    characteristic = Claw()
    manager.add_characteristic(characteristic)
    assert characteristic in manager.characteristics
