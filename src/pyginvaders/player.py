"""Player module for managing the player ship."""

import pygame

from pyginvaders.config import (
    PLAYER_COLOR,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    SCREEN_WIDTH,
)
from pyginvaders.game_object import GameObject


class Player(GameObject):
    """Represents the player's ship."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the player at the given position."""
        super().__init__(x, y)

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the player's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move_left(self) -> None:
        """Move the player left."""
        self.x -= PLAYER_SPEED

    def move_right(self) -> None:
        """Move the player right."""
        self.x += PLAYER_SPEED

    def clamp_to_bounds(self) -> None:
        """Keep player within screen bounds."""
        if self.x < 0:
            self.x = 0
        elif self.x + PLAYER_WIDTH > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - PLAYER_WIDTH

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""
        pygame.draw.rect(
            screen, PLAYER_COLOR, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        )
