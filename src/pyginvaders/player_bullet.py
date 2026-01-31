"""PlayerBullet module for managing player projectiles."""

import pygame

from pyginvaders.config import (
    PLAYER_BULLET_COLOR,
    PLAYER_BULLET_HEIGHT,
    PLAYER_BULLET_SPEED,
    PLAYER_BULLET_WIDTH,
)
from pyginvaders.game_object import GameObject


class PlayerBullet(GameObject):
    """Represents a bullet fired by the player."""

    def __init__(self) -> None:
        """Initialize an inactive bullet."""
        super().__init__(0, 0)
        self.active = False

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the bullet's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)

    def activate(self, x: int, y: int) -> None:
        """Activate the bullet at the given position."""
        self.x = x
        self.y = y
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the bullet."""
        self.active = False

    def update(self) -> None:
        """Update bullet position and deactivate if off screen."""
        if self.active:
            self.y -= PLAYER_BULLET_SPEED
            if self.y < 0:
                self.deactivate()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bullet on the screen if active."""
        if self.active:
            pygame.draw.rect(
                screen,
                PLAYER_BULLET_COLOR,
                (self.x, self.y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT),
            )
