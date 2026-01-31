"""Tests for the invader bullet module."""

from pyginvaders.config import SCREEN_HEIGHT
from pyginvaders.invader_bullet import InvaderBullet


def test_bullet_initialization():
    """Test that a bullet is initialized correctly."""
    bullet = InvaderBullet()
    assert bullet.x == 0
    assert bullet.y == 0
    assert bullet.active is False


def test_bullet_activation():
    """Test that activating a bullet sets position and makes it active."""
    bullet = InvaderBullet()
    bullet.activate(100, 200)
    assert bullet.x == 100
    assert bullet.y == 200
    assert bullet.active is True


def test_bullet_deactivation():
    """Test that deactivating a bullet makes it inactive."""
    bullet = InvaderBullet()
    bullet.activate(100, 200)
    bullet.deactivate()
    assert bullet.active is False


def test_bullet_movement():
    """Test that an active bullet moves down."""
    bullet = InvaderBullet()
    bullet.activate(100, 200)
    initial_y = bullet.y

    bullet.update()

    # Bullet should move down (positive y direction)
    assert bullet.y > initial_y
    assert bullet.active is True


def test_inactive_bullet_does_not_move():
    """Test that an inactive bullet does not move."""
    bullet = InvaderBullet()
    bullet.x = 100
    bullet.y = 200

    bullet.update()

    assert bullet.x == 100
    assert bullet.y == 200
    assert bullet.active is False


def test_bullet_deactivates_at_bottom_of_screen():
    """Test that bullet deactivates when it reaches bottom of screen."""
    bullet = InvaderBullet()
    bullet.activate(100, SCREEN_HEIGHT - 1)

    bullet.update()

    # Bullet should have moved past bottom and deactivated
    assert bullet.active is False


def test_bullet_remains_active_before_bottom():
    """Test that bullet remains active before reaching bottom."""
    bullet = InvaderBullet()
    bullet.activate(100, SCREEN_HEIGHT - 50)

    bullet.update()

    assert bullet.active is True


def test_get_rectangle():
    """Test that get_rectangle returns correct dimensions."""
    bullet = InvaderBullet()
    bullet.activate(100, 200)

    rect = bullet.get_rectangle()

    assert rect == (100, 200, 4, 20)  # x, y, width, height
