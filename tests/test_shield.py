"""Tests for the Shield class."""

from pyginvaders.config import SHIELD_HEIGHT, SHIELD_INITIAL_HEALTH, SHIELD_WIDTH
from pyginvaders.shield import Shield


def test_shield_initialization():
    """Test that a shield is initialized correctly."""
    shield = Shield(100, 200)
    assert shield.x == 100
    assert shield.y == 200
    assert shield.health == SHIELD_INITIAL_HEALTH


def test_shield_get_rectangle():
    """Test that get_rectangle returns correct dimensions."""
    shield = Shield(150, 250)
    rect = shield.get_rectangle()
    assert rect == (150, 250, SHIELD_WIDTH, SHIELD_HEIGHT)


def test_shield_get_rectangle_at_origin():
    """Test get_rectangle when shield is at origin."""
    shield = Shield(0, 0)
    rect = shield.get_rectangle()
    assert rect == (0, 0, SHIELD_WIDTH, SHIELD_HEIGHT)


def test_shield_take_damage():
    """Test that take_damage reduces health by 1."""
    shield = Shield(100, 200)
    initial_health = shield.health
    shield.take_damage()
    assert shield.health == initial_health - 1


def test_shield_take_damage_multiple_times():
    """Test that multiple hits reduce health correctly."""
    shield = Shield(100, 200)
    for i in range(3):
        shield.take_damage()
    assert shield.health == SHIELD_INITIAL_HEALTH - 3


def test_shield_health_cannot_go_below_zero():
    """Test that shield health is clamped to 0."""
    shield = Shield(100, 200)
    # Damage shield more times than it has health
    for _ in range(SHIELD_INITIAL_HEALTH + 5):
        shield.take_damage()
    assert shield.health == 0


def test_shield_is_destroyed_false_when_healthy():
    """Test that is_destroyed returns False when shield has health."""
    shield = Shield(100, 200)
    assert shield.is_destroyed() is False


def test_shield_is_destroyed_false_after_damage():
    """Test that is_destroyed returns False when shield still has health."""
    shield = Shield(100, 200)
    shield.take_damage()
    assert shield.is_destroyed() is False


def test_shield_is_destroyed_true_when_health_zero():
    """Test that is_destroyed returns True when health reaches 0."""
    shield = Shield(100, 200)
    # Reduce health to 0
    for _ in range(SHIELD_INITIAL_HEALTH):
        shield.take_damage()
    assert shield.is_destroyed() is True
