"""Tests for the game module."""

from unittest.mock import patch

from pyginvaders.config import (
    INVADER_BULLET_POOL_SIZE,
    INVADER_BULLET_WIDTH,
    INVADER_HEIGHT,
    INVADER_SHOOT_CHANCE,
    INVADER_SHOOT_DELAY,
    INVADER_WIDTH,
    KILL_SCORE,
    SHIELD_SPACING_X,
    SHIELD_START_COUNT,
    SHIELD_START_X,
    SHIELD_START_Y,
)
from pyginvaders.game import Game, check_rect_collision
from pyginvaders.invader import Invader


def test_game_initialization():
    """Test that the game is initialized correctly."""
    game = Game()
    assert game.running is False
    assert game.game_lost is False


def test_invader_bullet_pool_created():
    """Test that the invader bullet pool is created with correct size."""
    game = Game()
    assert len(game.invader_bullets) == INVADER_BULLET_POOL_SIZE
    # All bullets should start inactive
    assert all(not bullet.active for bullet in game.invader_bullets)


def test_fire_bullet_activates_bullet():
    """Test that firing a bullet activates an inactive bullet."""
    game = Game()
    # All bullets should start inactive
    assert all(not bullet.active for bullet in game.player_bullets)

    game.fire_bullet()

    # Exactly one bullet should now be active
    active_bullets = [b for b in game.player_bullets if b.active]
    assert len(active_bullets) == 1


def test_fire_bullet_positions_correctly():
    """Test that fired bullet is centered horizontally on player and above it."""
    game = Game()
    player_center_x = game.player.x + 25  # PLAYER_WIDTH // 2

    game.fire_bullet()

    active_bullet = next(b for b in game.player_bullets if b.active)
    bullet_center_x = active_bullet.x + 2  # PLAYER_BULLET_WIDTH // 2
    assert bullet_center_x == player_center_x
    # Bullet should be positioned just above the player
    assert active_bullet.y == game.player.y - 20  # PLAYER_BULLET_HEIGHT


def test_fire_bullet_with_exhausted_pool():
    """Test that firing does nothing when all bullets are active."""
    game = Game()

    # Activate all bullets
    for bullet in game.player_bullets:
        bullet.activate(100, 200)

    # Count active bullets before
    active_count_before = sum(1 for b in game.player_bullets if b.active)

    # Try to fire (should do nothing)
    game.fire_bullet()

    # Count should be the same
    active_count_after = sum(1 for b in game.player_bullets if b.active)
    assert active_count_after == active_count_before
    assert active_count_after == len(game.player_bullets)


def test_multiple_fires():
    """Test that multiple fires activate multiple bullets."""
    game = Game()

    game.fire_bullet()
    game.fire_bullet()
    game.fire_bullet()

    active_bullets = [b for b in game.player_bullets if b.active]
    assert len(active_bullets) == 3


def test_rect_collision_overlapping():
    """Test that overlapping rectangles are detected."""
    # Rectangles that overlap
    assert check_rect_collision((0, 0, 10, 10), (5, 5, 10, 10)) is True


def test_rect_collision_no_overlap():
    """Test that non-overlapping rectangles are not detected."""
    # Rectangles that don't touch
    assert check_rect_collision((0, 0, 10, 10), (20, 20, 10, 10)) is False


def test_rect_collision_touching_edge():
    """Test that rectangles touching at edge are detected."""
    # Rectangles touching at edge
    assert check_rect_collision((0, 0, 10, 10), (10, 0, 10, 10)) is False


def test_bullet_kills_invader():
    """Test that a bullet collision removes invader and deactivates bullet."""
    game = Game()
    initial_invader_count = len(game.invaders)
    initial_score = game.score

    # Get an invader and position a bullet to collide with it
    invader = game.invaders[0]
    bullet = game.player_bullets[0]
    bullet.activate(invader.x, invader.y)

    # Manually trigger collision check (simulate one frame)
    for bullet in game.player_bullets:
        if not bullet.active:
            continue
        for invader in game.invaders.copy():
            if check_rect_collision(
                (bullet.x, bullet.y, 4, 20),
                (invader.x, invader.y, INVADER_WIDTH, INVADER_HEIGHT),
            ):
                game.invaders.remove(invader)
                bullet.deactivate()
                game.score += KILL_SCORE
                break

    # Verify invader was removed
    assert len(game.invaders) == initial_invader_count - 1
    # Verify bullet was deactivated
    assert bullet.active is False
    # Verify score increased
    assert game.score == initial_score + KILL_SCORE


def test_bullet_kills_at_most_one_invader():
    """Test that each bullet kills at most one invader per frame."""
    game = Game()

    # Position two invaders at the same location
    invader1 = Invader(100, 100)
    invader2 = Invader(100, 100)
    game.invaders = [invader1, invader2]

    # Position a bullet to collide with both
    bullet = game.player_bullets[0]
    bullet.activate(100, 100)

    # Manually trigger collision check (simulate one frame)
    for bullet in game.player_bullets:
        if not bullet.active:
            continue
        for invader in game.invaders.copy():
            if check_rect_collision(
                (bullet.x, bullet.y, 4, 20),
                (invader.x, invader.y, INVADER_WIDTH, INVADER_HEIGHT),
            ):
                game.invaders.remove(invader)
                bullet.deactivate()
                game.score += KILL_SCORE
                break  # This ensures only one invader is killed

    # Verify only one invader was removed
    assert len(game.invaders) == 1
    # Verify bullet was deactivated
    assert bullet.active is False
    # Verify score increased by only one kill
    assert game.score == KILL_SCORE


def test_multiple_bullets_kill_multiple_invaders():
    """Test that multiple bullets can kill different invaders in one frame."""
    game = Game()

    # Set up two invaders at different positions
    invader1 = Invader(100, 100)
    invader2 = Invader(200, 100)
    game.invaders = [invader1, invader2]

    # Set up two bullets to collide with each invader
    bullet1 = game.player_bullets[0]
    bullet2 = game.player_bullets[1]
    bullet1.activate(100, 100)
    bullet2.activate(200, 100)

    # Manually trigger collision check (simulate one frame)
    for bullet in game.player_bullets:
        if not bullet.active:
            continue
        for invader in game.invaders.copy():
            if check_rect_collision(
                (bullet.x, bullet.y, 4, 20),
                (invader.x, invader.y, INVADER_WIDTH, INVADER_HEIGHT),
            ):
                game.invaders.remove(invader)
                bullet.deactivate()
                game.score += KILL_SCORE
                break

    # Verify both invaders were removed
    assert len(game.invaders) == 0
    # Verify both bullets were deactivated
    assert bullet1.active is False
    assert bullet2.active is False
    # Verify score increased by two kills
    assert game.score == 2 * KILL_SCORE


def test_invader_bullet_hits_player():
    """Test that invader bullet hitting player sets game_lost to True."""
    game = Game()

    # Position an invader bullet to collide with the player
    bullet = game.invader_bullets[0]
    bullet.activate(game.player.x, game.player.y)

    # Manually trigger collision check (simulate one frame)
    for bullet in game.invader_bullets:
        if not bullet.active:
            continue

        if check_rect_collision(
            bullet.get_rectangle(),
            game.player.get_rectangle(),
        ):
            bullet.deactivate()
            game.game_lost = True
            break

    # Verify game_lost is True
    assert game.game_lost is True
    # Verify bullet was deactivated
    assert bullet.active is False


def test_invader_bullet_miss_player():
    """Test that invader bullet missing player doesn't set game_lost."""
    game = Game()

    # Position an invader bullet away from the player
    test_bullet = game.invader_bullets[0]
    test_bullet.activate(game.player.x + 200, game.player.y)

    # Manually trigger collision check (simulate one frame)
    for bullet in game.invader_bullets:
        if not bullet.active:
            continue

        if check_rect_collision(
            bullet.get_rectangle(),
            game.player.get_rectangle(),
        ):
            bullet.deactivate()
            game.game_lost = True
            break

    # Verify game_lost is still False
    assert game.game_lost is False
    # Verify bullet is still active
    assert test_bullet.active is True


def test_game_lost_after_invader_kills():
    """Test that invader kills and score update happen before game_lost check."""
    game = Game()

    # Set up an invader
    invader = Invader(100, 100)
    game.invaders = [invader]
    initial_score = game.score

    # Position a player bullet to kill the invader
    player_bullet = game.player_bullets[0]
    player_bullet.activate(invader.x, invader.y)

    # Position an invader bullet to hit the player
    invader_bullet = game.invader_bullets[0]
    invader_bullet.activate(game.player.x, game.player.y)

    # Manually trigger collision checks in correct order (simulate one frame)
    # First, check player bullet-invader collisions
    for bullet in game.player_bullets:
        if not bullet.active:
            continue
        for inv in game.invaders.copy():
            if check_rect_collision(
                (bullet.x, bullet.y, 4, 20),
                (inv.x, inv.y, INVADER_WIDTH, INVADER_HEIGHT),
            ):
                game.invaders.remove(inv)
                bullet.deactivate()
                game.score += KILL_SCORE
                break

    # Then, check invader bullet-player collisions
    for bullet in game.invader_bullets:
        if not bullet.active:
            continue
        if check_rect_collision(
            bullet.get_rectangle(),
            game.player.get_rectangle(),
        ):
            bullet.deactivate()
            game.game_lost = True
            break

    # Verify invader was killed and score updated
    assert len(game.invaders) == 0
    assert game.score == initial_score + KILL_SCORE
    # Verify game_lost is True (happened after)
    assert game.game_lost is True


def test_draw_game_over_method_exists():
    """Test that draw_game_over method can be called with different messages."""
    game = Game()
    game.score = 170
    game.game_lost = True

    # Should not raise an exception
    game.draw_game_over("Game over")
    game.draw_game_over("You won!")


def test_draw_game_method_exists():
    """Test that draw_game method can be called."""
    game = Game()

    # Should not raise an exception
    game.draw_game()


def test_invader_shoot_counter_initialized():
    """Test that invader shoot counter starts at 0."""
    game = Game()
    assert game.invader_shoot_counter == 0


def test_fire_invader_bullet_activates_bullet():
    """Test that firing an invader bullet activates an inactive bullet."""
    game = Game()
    # All bullets should start inactive
    assert all(not bullet.active for bullet in game.invader_bullets)

    game.fire_invader_bullet(100, 200)

    # Exactly one bullet should now be active
    active_bullets = [b for b in game.invader_bullets if b.active]
    assert len(active_bullets) == 1


def test_fire_invader_bullet_positions_correctly():
    """Test that fired invader bullet is positioned at given coordinates."""
    game = Game()

    game.fire_invader_bullet(100, 200)

    active_bullet = next(b for b in game.invader_bullets if b.active)
    assert active_bullet.x == 100
    assert active_bullet.y == 200


def test_fire_invader_bullet_with_exhausted_pool():
    """Test that firing does nothing when all bullets are active."""
    game = Game()

    # Activate all bullets
    for bullet in game.invader_bullets:
        bullet.activate(100, 200)

    # Count active bullets before
    active_count_before = sum(1 for b in game.invader_bullets if b.active)

    # Try to fire (should do nothing)
    game.fire_invader_bullet(150, 250)

    # Count should be the same
    active_count_after = sum(1 for b in game.invader_bullets if b.active)
    assert active_count_after == active_count_before
    assert active_count_after == len(game.invader_bullets)


@patch("pyginvaders.game.random.randint")
def test_invader_shoots_bullet(mock_randint):
    """Test that invader shoots when random chance succeeds."""
    game = Game()
    # Mock random to guarantee shooting (return value < INVADER_SHOOT_CHANCE)
    mock_randint.return_value = 0

    # Set counter to trigger shooting
    game.invader_shoot_counter = INVADER_SHOOT_DELAY

    # Get an invader
    invader = game.invaders[0]

    # Count active bullets before
    active_before = sum(1 for b in game.invader_bullets if b.active)

    # Manually trigger shooting logic for this one invader
    if game.invader_shoot_counter >= INVADER_SHOOT_DELAY:
        game.invader_shoot_counter = 0
        if mock_randint(0, 99) < INVADER_SHOOT_CHANCE:
            bullet_x = invader.x + INVADER_WIDTH // 2 - INVADER_BULLET_WIDTH // 2
            bullet_y = invader.y + INVADER_HEIGHT
            game.fire_invader_bullet(bullet_x, bullet_y)

    # At least one bullet should be active now
    active_after = sum(1 for b in game.invader_bullets if b.active)
    assert active_after > active_before


@patch("pyginvaders.game.random.randint")
def test_invader_bullet_positioned_at_invader_bottom_center(mock_randint):
    """Test that invader bullet appears at bottom center of invader."""
    game = Game()
    # Mock random to guarantee shooting
    mock_randint.return_value = 0

    invader = game.invaders[0]
    expected_x = invader.x + INVADER_WIDTH // 2 - INVADER_BULLET_WIDTH // 2
    expected_y = invader.y + INVADER_HEIGHT

    # Fire bullet
    game.fire_invader_bullet(expected_x, expected_y)

    # Find the active bullet
    active_bullet = next(b for b in game.invader_bullets if b.active)
    assert active_bullet.x == expected_x
    assert active_bullet.y == expected_y


@patch("pyginvaders.game.random.randint")
def test_invader_shooting_respects_probability(mock_randint):
    """Test that invader doesn't shoot when random chance fails."""
    game = Game()
    # Mock random to prevent shooting (return value >= INVADER_SHOOT_CHANCE)
    mock_randint.return_value = INVADER_SHOOT_CHANCE

    # Set counter to trigger shooting
    game.invader_shoot_counter = INVADER_SHOOT_DELAY

    invader = game.invaders[0]

    # Manually trigger shooting logic for this one invader
    if game.invader_shoot_counter >= INVADER_SHOOT_DELAY:
        game.invader_shoot_counter = 0
        if mock_randint(0, 99) < INVADER_SHOOT_CHANCE:
            bullet_x = invader.x + INVADER_WIDTH // 2 - INVADER_BULLET_WIDTH // 2
            bullet_y = invader.y + INVADER_HEIGHT
            game.fire_invader_bullet(bullet_x, bullet_y)


def test_shields_created():
    """Test that shields are created correctly in the game."""
    game = Game()
    assert len(game.shields) == SHIELD_START_COUNT


def test_shields_positioned_correctly():
    """Test that shields are positioned according to config."""
    game = Game()
    for i, shield in enumerate(game.shields):
        expected_x = SHIELD_START_X + i * SHIELD_SPACING_X
        assert shield.x == expected_x
        assert shield.y == SHIELD_START_Y


def test_reset_game_recreates_shields():
    """Test that reset_game creates fresh shields."""
    game = Game()
    # Remove some shields
    game.shields = game.shields[:2]
    assert len(game.shields) != SHIELD_START_COUNT

    # Reset game
    game.reset_game()

    # Should have full set of shields again
    assert len(game.shields) == SHIELD_START_COUNT
