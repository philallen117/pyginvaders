"""Player module for managing the player ship."""

import pygame


class Player:
    """Represents the player's ship."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the player at the given position."""
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.color = (0, 0, 255)  # Blue
        self.speed = 5

    def move_left(self) -> None:
        """Move the player left."""
        self.x -= self.speed

    def move_right(self) -> None:
        """Move the player right."""
        self.x += self.speed

    def clamp_to_bounds(self, screen_width: int) -> None:
        """Keep player within screen bounds."""
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen_width:
            self.x = screen_width - self.width

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
