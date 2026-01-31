"""Invader module for managing alien invaders."""

import pygame

from pyginvaders.config import INVADER_COLOR, INVADER_HEIGHT, INVADER_WIDTH
from pyginvaders.game_object import GameObject


class Invader(GameObject):
    """Represents an alien invader."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the invader at the given position."""
        super().__init__(x, y)

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the invader's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, INVADER_WIDTH, INVADER_HEIGHT)

    def update(self, direction: int, speed: int) -> None:
        """Update the invader's position.

        Args:
            direction: Direction to move (1 for right, -1 for left)
            speed: Number of pixels to move
        """
        self.x += direction * speed

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the invader on the screen."""
        pygame.draw.rect(
            screen, INVADER_COLOR, (self.x, self.y, INVADER_WIDTH, INVADER_HEIGHT)
        )
