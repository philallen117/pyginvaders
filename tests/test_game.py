"""Tests for the game module."""

from pyginvaders.game import Game


def test_game_initialization():
    """Test that the game is initialized correctly."""
    game = Game()
    assert game.running is False
