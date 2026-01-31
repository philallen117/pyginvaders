"""Game module containing the main game loop."""

import pygame

from pyginvaders.config import (
    FPS,
    INVADER_COLS,
    INVADER_DROP_DISTANCE,
    INVADER_MOVE_DELAY,
    INVADER_ROWS,
    INVADER_SPACING_X,
    INVADER_SPACING_Y,
    INVADER_SPEED_X,
    INVADER_START_X,
    INVADER_START_Y,
    INVADER_WIDTH,
    PLAYER_BULLET_HEIGHT,
    PLAYER_BULLET_POOL_SIZE,
    PLAYER_BULLET_WIDTH,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from pyginvaders.invader import Invader
from pyginvaders.player import Player
from pyginvaders.player_bullet import PlayerBullet


class Game:
    """Main game class that manages the game state and loop."""

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PygInvaders")
        self.clock = pygame.time.Clock()
        self.running = False

        # Create player at bottom center of screen
        player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        player_y = SCREEN_HEIGHT - 60  # 60 pixels from bottom
        self.player = Player(player_x, player_y)

        # Create player bullet pool
        self.player_bullets = [PlayerBullet() for _ in range(PLAYER_BULLET_POOL_SIZE)]

        # Create invader grid
        self.invaders = []
        for row in range(INVADER_ROWS):
            for col in range(INVADER_COLS):
                x = INVADER_START_X + col * INVADER_SPACING_X
                y = INVADER_START_Y + row * INVADER_SPACING_Y
                self.invaders.append(Invader(x, y))

        # Invader movement state
        self.invader_direction = 1  # 1 for right, -1 for left
        self.invader_move_counter = 0  # counts frames until next move

    def fire_bullet(self) -> None:
        """Fire a bullet from the player if one is available in the pool."""
        # Find first inactive bullet
        for bullet in self.player_bullets:
            if not bullet.active:
                # Position bullet centered on player, just above it
                bullet_x = self.player.x + PLAYER_WIDTH // 2 - PLAYER_BULLET_WIDTH // 2
                bullet_y = self.player.y - PLAYER_BULLET_HEIGHT
                bullet.activate(bullet_x, bullet_y)
                break

    def run(self) -> None:
        """Start the game loop."""
        self.running = True
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fire_bullet()

            # Handle continuous key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            # Keep player within bounds
            self.player.clamp_to_bounds()

            # Update bullets
            for bullet in self.player_bullets:
                bullet.update()

            # Update invaders
            self.invader_move_counter += 1
            if self.invader_move_counter >= INVADER_MOVE_DELAY:
                self.invader_move_counter = 0
                for invader in self.invaders:
                    invader.update(self.invader_direction, INVADER_SPEED_X)

                # Check if any invader reached the edge
                hit_edge = False
                for invader in self.invaders:
                    if invader.x <= 0 or invader.x + INVADER_WIDTH >= SCREEN_WIDTH:
                        hit_edge = True
                        break

                # If edge was hit, undo horizontal move, drop, and reverse direction
                if hit_edge:
                    for invader in self.invaders:
                        invader.x -= self.invader_direction * INVADER_SPEED_X
                        invader.y += INVADER_DROP_DISTANCE
                    self.invader_direction *= -1

            # Fill screen with black
            self.screen.fill((0, 0, 0))

            # Draw invaders
            for invader in self.invaders:
                invader.draw(self.screen)

            # Draw player
            self.player.draw(self.screen)

            # Draw bullets
            for bullet in self.player_bullets:
                bullet.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Cap at 60 FPS
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()
