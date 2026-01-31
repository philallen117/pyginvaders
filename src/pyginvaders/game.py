"""Game module containing the main game loop."""

import random

import pygame

from pyginvaders.config import (
    FPS,
    GAME_OVER_TEXT_FONT_POINT_SIZE,
    INVADER_BULLET_POOL_SIZE,
    INVADER_BULLET_WIDTH,
    INVADER_COLS,
    INVADER_DROP_DISTANCE,
    INVADER_HEIGHT,
    INVADER_MOVE_DELAY,
    INVADER_ROWS,
    INVADER_SHOOT_CHANCE,
    INVADER_SHOOT_DELAY,
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
    SHIELD_SPACING_X,
    SHIELD_START_COUNT,
    SHIELD_START_X,
    SHIELD_START_Y,
    TEXT_COLOR,
)
from pyginvaders.invader import Invader
from pyginvaders.invader_bullet import InvaderBullet
from pyginvaders.player import Player
from pyginvaders.player_bullet import PlayerBullet
from pyginvaders.shield import Shield


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

        # Initialize fonts (only needed once)
        self.font = pygame.font.Font(None, SCORE_TEXT_FONT_POINT_SIZE)
        self.game_over_font = pygame.font.Font(None, GAME_OVER_TEXT_FONT_POINT_SIZE)

        # Initialize game state
        self.reset_game()

    def reset_game(self) -> None:
        """Reset game state to starting conditions."""
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

        # Create shields
        self.shields = []
        for i in range(SHIELD_START_COUNT):
            x = SHIELD_START_X + i * SHIELD_SPACING_X
            y = SHIELD_START_Y
            self.shields.append(Shield(x, y))

        # Invader movement state
        self.invader_direction = 1  # 1 for right, -1 for left
        self.invader_move_counter = 0  # counts frames until next move
        self.invader_shoot_counter = 0  # counts frames until next shooting decision

        # Score
        self.score = 0

        # Game state
        self.game_lost = False
        self.player_won = False

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

    def fire_invader_bullet(self, x: int, y: int) -> None:
        """Fire a bullet from an invader if one is available in the pool.

        Args:
            x: X position for the bullet
            y: Y position for the bullet
        """
        # Find first inactive bullet
        for bullet in self.invader_bullets:
            if not bullet.active:
                bullet.activate(x, y)
                break

    def draw_game(self) -> None:
        """Draw the game scene."""
        # Fill screen with black
        self.screen.fill((0, 0, 0))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, SCORE_TEXT_POSITION)

        # Draw invaders
        for invader in self.invaders:
            invader.draw(self.screen)

        # Draw shields
        for shield in self.shields:
            shield.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)

        # Draw invader bullets
        for bullet in self.invader_bullets:
            bullet.draw(self.screen)

    def draw_game_over(self, message: str) -> None:
        """Draw the game over scene with a custom message.

        Args:
            message: The message to display (e.g., "Game over" or "You won!")
        """
        # Fill screen with black
        self.screen.fill((0, 0, 0))

        # Render message text
        message_text = self.game_over_font.render(message, True, TEXT_COLOR)
        message_rect = message_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        )

        # Render score text
        score_text = self.game_over_font.render(
            f"Score: {self.score}", True, TEXT_COLOR
        )
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Render restart prompt
        restart_text = self.font.render("Press R to restart", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        )

        # Draw all texts
        self.screen.blit(message_text, message_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def check_player_bullet_collisions(self) -> None:
        """Check for collisions between player bullets and invaders."""
        for bullet in self.player_bullets:
            if not bullet.active:
                continue

            bullet_rect = bullet.get_rectangle()
            for invader in self.invaders.copy():
                if check_rect_collision(bullet_rect, invader.get_rectangle()):
                    # Collision detected
                    self.invaders.remove(invader)
                    bullet.deactivate()
                    self.score += KILL_SCORE

                    # Check if all invaders are destroyed
                    if len(self.invaders) == 0:
                        self.player_won = True

                    return  # Bullet hit something, stop checking this bullet

    def check_invader_bullet_collisions(self) -> bool:
        """Check for collisions between invader bullets and player.

        Returns:
            True if player was hit (game should end), False otherwise
        """
        player_rect = self.player.get_rectangle()
        for bullet in self.invader_bullets:
            if not bullet.active:
                continue

            if check_rect_collision(bullet.get_rectangle(), player_rect):
                # Collision detected - game is lost
                bullet.deactivate()
                return True

        return False

    def check_invader_bullet_shield_collisions(self) -> None:
        """Check for collisions between invader bullets and shields."""
        for bullet in self.invader_bullets:
            if not bullet.active:
                continue

            bullet_rect = bullet.get_rectangle()
            # Use a copy to avoid modifying list during iteration
            for shield in self.shields.copy():
                if check_rect_collision(bullet_rect, shield.get_rectangle()):
                    # Collision detected
                    bullet.deactivate()
                    shield.take_damage()

                    # Remove shield if destroyed
                    if shield.is_destroyed():
                        self.shields.remove(shield)

                    break  # Bullet can only hit one shield

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
                    elif event.key == pygame.K_r:
                        # Restart the game if in game over or win state
                        if self.game_lost or self.player_won:
                            self.reset_game()

            # If game is lost, just draw game over screen and skip updates
            if self.game_lost:
                self.draw_game_over("Game over")
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            # If player won, draw win screen and skip updates
            if self.player_won:
                self.draw_game_over("You won!")
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

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

            # Check for collisions
            self.check_invader_bullet_shield_collisions()
            self.check_player_bullet_collisions()

            if self.check_invader_bullet_collisions():
                self.game_lost = True
                continue  # Skip to next frame to show game over screen

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

            # Invader shooting logic
            self.invader_shoot_counter += 1
            if self.invader_shoot_counter >= INVADER_SHOOT_DELAY:
                self.invader_shoot_counter = 0
                for invader in self.invaders:
                    # Each invader has INVADER_SHOOT_CHANCE% chance to shoot
                    if random.randint(0, 99) < INVADER_SHOOT_CHANCE:
                        # Calculate bullet position at bottom center of invader
                        bullet_x = (
                            invader.x + INVADER_WIDTH // 2 - INVADER_BULLET_WIDTH // 2
                        )
                        bullet_y = invader.y + INVADER_HEIGHT
                        self.fire_invader_bullet(bullet_x, bullet_y)

            # Draw game scene
            self.draw_game()

            # Update display
            pygame.display.flip()

            # Cap at 60 FPS
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()
