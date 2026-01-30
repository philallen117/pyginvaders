"""Tests for the player module."""

from pyginvaders.player import Player


def test_player_initialization():
    """Test that a player is initialized correctly."""
    player = Player(100, 200)
    assert player.x == 100
    assert player.y == 200
