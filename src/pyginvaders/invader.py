"""Invader module for managing alien invaders."""

import pygame

from pyginvaders.config import INVADER_COLOR, INVADER_HEIGHT, INVADER_WIDTH


class Invader:
    """Represents an alien invader."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the invader at the given position."""
        self.x = x
        self.y = y

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
