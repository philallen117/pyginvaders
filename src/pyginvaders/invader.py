"""Invader module for managing alien invaders."""


class Invader:
    """Represents an alien invader."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the invader at the given position."""
        self.x = x
        self.y = y
