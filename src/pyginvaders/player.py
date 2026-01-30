"""Player module for managing the player ship."""


class Player:
    """Represents the player's ship."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the player at the given position."""
        self.x = x
        self.y = y
