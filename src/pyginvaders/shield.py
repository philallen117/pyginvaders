"""Shield module for managing defensive shields."""

import pygame

from pyginvaders.config import (
    SHIELD_ALPHA_REDUCTION,
    SHIELD_COLOR,
    SHIELD_HEIGHT,
    SHIELD_INITIAL_HEALTH,
    SHIELD_WIDTH,
)
from pyginvaders.game_object import GameObject


class Shield(GameObject):
    """Represents a defensive shield that protects the player."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the shield at the given position.

        Args:
            x: X coordinate of the shield
            y: Y coordinate of the shield
        """
        super().__init__(x, y)
        self.health = SHIELD_INITIAL_HEALTH

    def get_rectangle(self) -> tuple[int, int, int, int]:
        """Get the shield's bounding rectangle.

        Returns:
            A tuple of (x, y, width, height)
        """
        return (self.x, self.y, SHIELD_WIDTH, SHIELD_HEIGHT)

    def take_damage(self) -> None:
        """Reduce shield health by 1 when hit by a bullet."""
        self.health = max(0, self.health - 1)

    def is_destroyed(self) -> bool:
        """Check if shield is destroyed.

        Returns:
            True if health is 0, False otherwise
        """
        return self.health == 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the shield on the screen with transparency based on health.

        Args:
            screen: The pygame surface to draw on
        """
        # Calculate alpha based on damage taken
        damage_taken = SHIELD_INITIAL_HEALTH - self.health
        alpha = 255 - (damage_taken * SHIELD_ALPHA_REDUCTION)
        alpha = max(0, min(255, alpha))  # Clamp to valid range

        # Create a surface with per-pixel alpha
        shield_surface = pygame.Surface((SHIELD_WIDTH, SHIELD_HEIGHT), pygame.SRCALPHA)

        # Draw rectangle on the surface with alpha
        color_with_alpha = (*SHIELD_COLOR, alpha)
        pygame.draw.rect(
            shield_surface, color_with_alpha, (0, 0, SHIELD_WIDTH, SHIELD_HEIGHT)
        )

        # Blit the transparent surface to the screen
        screen.blit(shield_surface, (self.x, self.y))
