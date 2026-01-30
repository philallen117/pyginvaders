"""Tests for the invader module."""

from pyginvaders.invader import Invader


def test_invader_initialization():
    """Test that an invader is initialized correctly."""
    invader = Invader(50, 75)
    assert invader.x == 50
    assert invader.y == 75
