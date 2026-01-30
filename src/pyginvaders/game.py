"""Game module containing the main game loop."""

import pygame

from pyginvaders.player import Player


class Game:
    """Main game class that manages the game state and loop."""

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PygInvaders")
        self.clock = pygame.time.Clock()
        self.running = False

        # Create player at bottom center of screen
        player_x = self.width // 2 - 25  # Center the 50-wide player
        player_y = self.height - 60  # 60 pixels from bottom
        self.player = Player(player_x, player_y)

    def run(self) -> None:
        """Start the game loop."""
        self.running = True
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle continuous key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            # Keep player within bounds
            self.player.clamp_to_bounds(self.width)

            # Fill screen with black
            self.screen.fill((0, 0, 0))

            # Draw player
            self.player.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Cap at 60 FPS
            self.clock.tick(60)

        # Clean up
        pygame.quit()
