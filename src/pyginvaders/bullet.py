"""Bullet module for managing projectiles."""


class Bullet:
    """Represents a bullet fired by the player or enemies."""

    def __init__(self, x: int, y: int, velocity: int) -> None:
        """Initialize the bullet at the given position with velocity."""
        self.x = x
        self.y = y
        self.velocity = velocity
