"""Bullet base class for managing projectiles."""

from abc import ABC, abstractmethod

import pygame

from pyginvaders.game_object import GameObject


class Bullet(GameObject, ABC):
    """Abstract base class for bullets."""

    def __init__(self) -> None:
        """Initialize an inactive bullet."""
        super().__init__(0, 0)
        self.active = False

    def activate(self, x: int, y: int) -> None:
        """Activate the bullet at the given position."""
        self.x = x
        self.y = y
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the bullet."""
        self.active = False

    @abstractmethod
    def update(self) -> None:
        """Update bullet position and state."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bullet on the screen."""
        pass

    @abstractmethod
    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the bullet's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        pass
