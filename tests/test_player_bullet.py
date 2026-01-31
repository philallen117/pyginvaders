"""Tests for the player_bullet module."""

from pyginvaders.player_bullet import PlayerBullet


def test_bullet_initialization():
    """Test that a bullet is initialized as inactive."""
    bullet = PlayerBullet()
    assert bullet.active is False


def test_bullet_activation():
    """Test that a bullet can be activated at a position."""
    bullet = PlayerBullet()
    bullet.activate(100, 200)
    assert bullet.active is True
    assert bullet.x == 100
    assert bullet.y == 200


def test_bullet_deactivation():
    """Test that a bullet can be deactivated."""
    bullet = PlayerBullet()
    bullet.activate(100, 200)
    bullet.deactivate()
    assert bullet.active is False


def test_bullet_movement():
    """Test that an active bullet moves upward."""
    bullet = PlayerBullet()
    bullet.activate(100, 200)
    initial_y = bullet.y
    bullet.update()
    assert bullet.y == initial_y - 5  # PLAYER_BULLET_SPEED is 5


def test_inactive_bullet_does_not_move():
    """Test that an inactive bullet does not move."""
    bullet = PlayerBullet()
    bullet.x = 100
    bullet.y = 200
    bullet.update()
    assert bullet.y == 200


def test_bullet_deactivates_at_top_of_screen():
    """Test that a bullet deactivates when it reaches the top of the screen."""
    bullet = PlayerBullet()
    bullet.activate(100, 3)  # Just above y=0
    bullet.update()  # Will move to y=-2
    assert bullet.active is False


def test_bullet_remains_active_before_top():
    """Test that a bullet remains active before reaching the top."""
    bullet = PlayerBullet()
    bullet.activate(100, 10)
    bullet.update()
    assert bullet.active is True
    assert bullet.y == 5
