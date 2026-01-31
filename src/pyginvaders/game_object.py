"""Base class for game objects."""

from abc import ABC, abstractmethod


class GameObject(ABC):
    """Abstract base class for game objects that can collide."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the game object at the given position.

        Args:
            x: X coordinate of the object
            y: Y coordinate of the object
        """
        self.x = x
        self.y = y

    @abstractmethod
    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the object's bounding rectangle for collision detection.

        Returns:
            A tuple of (x, y, width, height) representing the object's rectangle
        """
        pass
