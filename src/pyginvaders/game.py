"""Game module containing the main game loop."""

import pygame


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

        # Setup font and text
        self.font = pygame.font.SysFont(None, 48)
        self.text = self.font.render("Welcome to PygInvaders", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))

    def run(self) -> None:
        """Start the game loop."""
        self.running = True
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill screen with black
            self.screen.fill((0, 0, 0))

            # Draw centered text
            self.screen.blit(self.text, self.text_rect)

            # Update display
            pygame.display.flip()

            # Cap at 60 FPS
            self.clock.tick(60)

        # Clean up
        pygame.quit()
