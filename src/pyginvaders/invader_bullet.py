"""InvaderBullet module for managing invader projectiles."""

import pygame

from pyginvaders.bullet import Bullet
from pyginvaders.config import (
    INVADER_BULLET_COLOR,
    INVADER_BULLET_HEIGHT,
    INVADER_BULLET_SPEED,
    INVADER_BULLET_WIDTH,
    SCREEN_HEIGHT,
)


class InvaderBullet(Bullet):
    """Represents a bullet fired by an invader."""

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the bullet's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, INVADER_BULLET_WIDTH, INVADER_BULLET_HEIGHT)

    def update(self) -> None:
        """Update bullet position and deactivate if off screen."""
        if self.active:
            self.y += INVADER_BULLET_SPEED
            if self.y > SCREEN_HEIGHT:
                self.deactivate()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bullet on the screen if active."""
        if self.active:
            pygame.draw.rect(
                screen,
                INVADER_BULLET_COLOR,
                (self.x, self.y, INVADER_BULLET_WIDTH, INVADER_BULLET_HEIGHT),
            )
