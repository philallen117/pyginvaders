"""Tests for game restart functionality."""

import pygame

from pyginvaders.config import (
    INVADER_BULLET_POOL_SIZE,
    INVADER_COLS,
    INVADER_ROWS,
    PLAYER_BULLET_POOL_SIZE,
)
from pyginvaders.game import Game


def test_reset_game_reinitializes_player():
    """Test that reset_game creates a new player at starting position."""
    game = Game()
    original_player_x = game.player.x
    original_player_y = game.player.y

    # Move player
    game.player.x += 100
    assert game.player.x != original_player_x

    # Reset game
    game.reset_game()

    # Player should be back at starting position
    assert game.player.x == original_player_x
    assert game.player.y == original_player_y


def test_reset_game_clears_score():
    """Test that reset_game resets score to zero."""
    game = Game()
    game.score = 1000

    game.reset_game()

    assert game.score == 0


def test_reset_game_resets_bullets():
    """Test that reset_game creates fresh bullet pools."""
    game = Game()

    # Activate some bullets
    game.player_bullets[0].activate(100, 100)
    game.invader_bullets[0].activate(200, 200)
    assert game.player_bullets[0].active
    assert game.invader_bullets[0].active

    # Reset game
    game.reset_game()

    # All bullets should be inactive
    assert all(not bullet.active for bullet in game.player_bullets)
    assert all(not bullet.active for bullet in game.invader_bullets)
    assert len(game.player_bullets) == PLAYER_BULLET_POOL_SIZE
    assert len(game.invader_bullets) == INVADER_BULLET_POOL_SIZE


def test_reset_game_recreates_invaders():
    """Test that reset_game creates a fresh invader grid."""
    game = Game()
    expected_invader_count = INVADER_ROWS * INVADER_COLS

    # Remove some invaders
    game.invaders = game.invaders[:5]
    assert len(game.invaders) != expected_invader_count

    # Reset game
    game.reset_game()

    # Should have full grid again
    assert len(game.invaders) == expected_invader_count


def test_reset_game_resets_game_state_flags():
    """Test that reset_game resets game over and win flags."""
    game = Game()

    game.game_lost = True
    game.player_won = True

    game.reset_game()

    assert game.game_lost is False
    assert game.player_won is False


def test_reset_game_resets_invader_movement_state():
    """Test that reset_game resets invader direction and counters."""
    game = Game()

    # Modify invader state
    game.invader_direction = -1
    game.invader_move_counter = 50
    game.invader_shoot_counter = 30

    game.reset_game()

    assert game.invader_direction == 1
    assert game.invader_move_counter == 0
    assert game.invader_shoot_counter == 0


def test_restart_from_game_over_state():
    """Test that pressing R in game over state restarts the game."""
    game = Game()
    game.running = True
    game.game_lost = True
    game.score = 500

    # Simulate R key press
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    # Process one frame
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game.game_lost or game.player_won:
                game.reset_game()

    # Game should be reset
    assert game.game_lost is False
    assert game.score == 0
    assert len(game.invaders) == INVADER_ROWS * INVADER_COLS


def test_restart_from_win_state():
    """Test that pressing R in win state restarts the game."""
    game = Game()
    game.running = True
    game.player_won = True
    game.score = 1500
    game.invaders = []  # All invaders destroyed

    # Simulate R key press
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    # Process one frame
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game.game_lost or game.player_won:
                game.reset_game()

    # Game should be reset
    assert game.player_won is False
    assert game.score == 0
    assert len(game.invaders) == INVADER_ROWS * INVADER_COLS


def test_r_key_does_not_restart_during_active_game():
    """Test that R key has no effect during normal gameplay."""
    game = Game()
    game.running = True
    game.score = 100
    original_invader_count = len(game.invaders)

    # Remove one invader to change state
    game.invaders.pop()
    assert len(game.invaders) == original_invader_count - 1

    # Simulate R key press (should not restart since game is active)
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    # Process event with same logic as game loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game.game_lost or game.player_won:
                game.reset_game()

    # Game state should be unchanged
    assert game.score == 100
    assert len(game.invaders) == original_invader_count - 1
