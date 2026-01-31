"""Invader module for managing alien invaders."""

import pygame

from pyginvaders.config import INVADER_COLOR, INVADER_HEIGHT, INVADER_WIDTH


class Invader:
    """Represents an alien invader."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the invader at the given position."""
        self.x = x
        self.y = y
        self.alive = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the invader on the screen if alive."""
        if self.alive:
            pygame.draw.rect(
                screen, INVADER_COLOR, (self.x, self.y, INVADER_WIDTH, INVADER_HEIGHT)
            )
