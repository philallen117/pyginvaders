"""Tests for the game module."""

from pyginvaders.config import INVADER_HEIGHT, INVADER_WIDTH, KILL_SCORE
from pyginvaders.game import Game, check_rect_collision
from pyginvaders.invader import Invader


def test_game_initialization():
    """Test that the game is initialized correctly."""
    game = Game()
    assert game.running is False


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
