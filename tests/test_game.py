"""Tests for the game module."""

from pyginvaders.game import Game


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
