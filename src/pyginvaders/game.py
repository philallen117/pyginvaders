"""Game module containing the main game loop."""

import pygame

from pyginvaders.config import (
    FPS,
    INVADER_BULLET_POOL_SIZE,
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
    KILL_SCORE,
    PLAYER_BULLET_HEIGHT,
    PLAYER_BULLET_POOL_SIZE,
    PLAYER_BULLET_WIDTH,
    PLAYER_WIDTH,
    SCORE_TEXT_FONT_POINT_SIZE,
    SCORE_TEXT_POSITION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TEXT_COLOR,
)
from pyginvaders.invader import Invader
from pyginvaders.invader_bullet import InvaderBullet
from pyginvaders.player import Player
from pyginvaders.player_bullet import PlayerBullet


def check_rect_collision(
    rect1: tuple[int, int, int, int], rect2: tuple[int, int, int, int]
) -> bool:
    """Check if two rectangles collide using AABB collision detection.

    Args:
        rect1: First rectangle as (x, y, width, height)
        rect2: Second rectangle as (x, y, width, height)

    Returns:
        True if rectangles overlap, False otherwise
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2


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

        # Create invader bullet pool
        self.invader_bullets = [
            InvaderBullet() for _ in range(INVADER_BULLET_POOL_SIZE)
        ]

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

        # Score
        self.score = 0
        self.font = pygame.font.Font(None, SCORE_TEXT_FONT_POINT_SIZE)

        # Game state
        self.game_lost = False

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

            # Update invader bullets
            for bullet in self.invader_bullets:
                bullet.update()

            # Check player bullet - invader collisions
            for bullet in self.player_bullets:
                if not bullet.active:
                    continue

                bullet_rect = bullet.get_rectangle()
                for (
                    invader
                ) in self.invaders.copy():  # Copy to safely remove during iteration
                    if check_rect_collision(bullet_rect, invader.get_rectangle()):
                        # Collision detected
                        self.invaders.remove(invader)
                        bullet.deactivate()
                        self.score += KILL_SCORE
                        break  # Exit invader loop; continue checking other bullets

            # Check invader bullet - player collisions
            player_rect = self.player.get_rectangle()
            for bullet in self.invader_bullets:
                if not bullet.active:
                    continue

                if check_rect_collision(bullet.get_rectangle(), player_rect):
                    # Collision detected - game is lost
                    bullet.deactivate()
                    self.game_lost = True
                    break  # Exit bullet loop

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

            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, SCORE_TEXT_POSITION)

            # Draw invaders
            for invader in self.invaders:
                invader.draw(self.screen)

            # Draw player
            self.player.draw(self.screen)

            # Draw bullets
            for bullet in self.player_bullets:
                bullet.draw(self.screen)

            # Draw invader bullets
            for bullet in self.invader_bullets:
                bullet.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Cap at 60 FPS
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()
