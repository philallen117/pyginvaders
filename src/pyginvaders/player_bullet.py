"""PlayerBullet module for managing player projectiles."""

import pygame

from pyginvaders.bullet import Bullet
from pyginvaders.config import (
    PLAYER_BULLET_COLOR,
    PLAYER_BULLET_HEIGHT,
    PLAYER_BULLET_SPEED,
    PLAYER_BULLET_WIDTH,
)


class PlayerBullet(Bullet):
    """Represents a bullet fired by the player."""

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the bullet's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)

    def update(self) -> None:
        """Update bullet position and deactivate if off screen."""
        if self.active:
            self.y += PLAYER_BULLET_SPEED
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
